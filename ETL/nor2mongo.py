import pandas as pd
import pyodbc
from pymongo import MongoClient
from datetime import datetime

# --- 1️⃣ Conexión a SQL Server (en Docker) ---
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

# --- 2️⃣ Conexión a MongoDB ---
def connect_mongo():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["North"]  # ✅ devuelve la base de datos
    return db

# --- 3️⃣ Extracción de datos relevantes ---
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

# --- 4️⃣ Limpieza de fechas ---
def fix_dates(val):
    if val is pd.NaT or pd.isna(val):
        return None
    if isinstance(val, pd.Timestamp):
        return datetime(val.year, val.month, val.day, val.hour, val.minute, val.second)
    return val

# --- 5️⃣ Cargar datos en Mongo ---
def load_to_mongo(dfs, db):
    print("Cargando datos en MongoDB (una colección por tabla)...")

    for name, df in dfs.items():
        collection = db[name]  # ✅ crea/usa una colección por tabla
        collection.delete_many({})  # limpia la colección

        print(f"\n📦 Procesando tabla: {name} ({len(df)} filas)")

        # ✅ Convertir datetimes y NaT -> None
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].apply(lambda x: fix_dates(x))

        # ✅ Convertir a registros
        records = df.to_dict("records")

        # 🔍 Verificación de tipos
        for col in df.columns:
            tipos = list({type(v) for v in df[col]})
            print(f"  • Columna {col}: {tipos}")

        # ✅ Inserción a Mongo
        if records:
            print(f"  Insertando {len(records)} registros en colección '{name}' ...")
            try:
                collection.insert_many(records)
                print(f"  ✅ Colección '{name}' insertada correctamente.")
            except Exception as e:
                print(f"  ❌ Error insertando '{name}': {e}")
        else:
            print(f"  ⚠️ Tabla {name} vacía, nada que insertar.")

    print("\n✅ Proceso de carga completado exitosamente.")

# --- 6️⃣ Ejecución principal ---
def main():
    print("Conectando a SQL Server (Docker)...")
    conn = connect_sqlserver()

    print("Extrayendo datos de Northwind...")
    dfs = extract_data(conn)

    print("Conectando a MongoDB...")
    db = connect_mongo()

    print("Cargando datos en MongoDB...")
    load_to_mongo(dfs, db)

    print("Proceso ETL completado exitosamente 🚀")

if __name__ == "__main__":
    main()
