import pandas as pd
import pyodbc
from pymongo import MongoClient
from datetime import datetime

# --- 1 Conexión a SQL Server (en Docker) ---
def connect_sqlserver():
    conn_str = (
        "DRIVER={SQL SERVER};"
        "SERVER=localhost,1433;"
        "DATABASE=Northwind;"
        "UID=SA;"
        "PWD=YourStrong!Passw0rd;"
        "Encrypt=no;"
    )
    return pyodbc.connect(conn_str)

# --- 2 Conexión a MongoDB ---
def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["North"]  # devuelve la base de datos
    return db

# --- 3 Extracción de datos relevantes ---
def extract_data(conn):
    queries = {
        "orders": """
            SELECT OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipCountry, ShipCity
            FROM Orders
        """,
        "order_details": """
            SELECT OrderID, ProductID, UnitPrice, Quantity, Discount
            FROM [Order Details]
        """,
        "customers": """
            SELECT CustomerID, CompanyName, ContactName, Country, City, Region
            FROM Customers
        """,
        "products": """
            SELECT ProductID, ProductName, CategoryID, SupplierID, UnitPrice
            FROM Products
        """,
        "categories": """
            SELECT CategoryID, CategoryName, Description
            FROM Categories
        """,
        "employees": """
            SELECT EmployeeID, FirstName, LastName, Title, Country
            FROM Employees
        """,
        "suppliers": """
            SELECT SupplierID, CompanyName AS SupplierName, Country AS SupplierCountry
            FROM Suppliers
        """
    }

    dfs = {}
    for name, query in queries.items():
        print(f"Extrayendo {name}...")
        dfs[name] = pd.read_sql(query, conn)
    return dfs

# --- 4 Limpieza de fechas ---
def transform_records(df: pd.DataFrame) -> list:
    records = df.to_dict("records")
    for r in records:
        for k, v in r.items():
            if isinstance(v, pd.Timestamp):
                r[k] = v.to_pydatetime()  # datetime.datetime nativo
            elif pd.isna(v):
                r[k] = None  # NaT -> None
    return records

# --- 5 Cargar datos en Mongo ---
def load_to_mongo(dfs, db):
    print("Cargando datos en MongoDB (una colección por tabla)...")

    for name, df in dfs.items():
        collection = db[name]  # crea/usa una colección por tabla
        collection.delete_many({})  # limpia la colección

        print(f"\n Procesando tabla: {name} ({len(df)} filas)")

        # Convertir a registros
        records = transform_records(df)

        # Inserción a Mongo
        if records:
            print(f"  Insertando {len(records)} registros en colección '{name}' ...")
            try:
                collection.insert_many(records)
                print(f"---Colección '{name}' insertado correctamente")
                
            except Exception as e:
                print(f"Error insertando '{name}': {e}")
        else:
            print(f" Tabla {name} vacía, nada que insertar.")

    

# --- 6 Ejecución principal ---
def main():
    print("Conectando a SQL Server (Docker)...")
    conn = connect_sqlserver()

    print("Extrayendo datos de Northwind...")
    dfs = extract_data(conn)

    print("Conectando a MongoDB...")
    db = connect_mongo()

    print("Cargando datos en MongoDB...")
    load_to_mongo(dfs, db)

    print("\nProceso ETL completado exitosamente")

if __name__ == "__main__":
    main()
