from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import math

# --- Configuración MongoDB ---
mongo_host = "localhost"
mongo_port = 27017
mongo_db = "North"

dim_collections = ["Customers", "Products", "Categories", "Suppliers", "Employees"]
orders_collection = "Orders"
order_details_collection = "Order_details"

client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]

# --- Configuración Elasticsearch ---
es = Elasticsearch("http://localhost:9200")
if not es.ping():
    raise ValueError("No se puede conectar a Elasticsearch")

# --- Función para construir dimensión tiempo ---
def build_time_dim(date_val):
    if not date_val:
        return None
    
    # Si ya es un datetime, úsalo directamente
    if isinstance(date_val, datetime):
        date_obj = date_val
    # Si es string, intenta parsear con los dos posibles formatos
    elif isinstance(date_val, str):
        try:
            if "." in date_val:
                date_obj = datetime.strptime(date_val, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                date_obj = datetime.strptime(date_val, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            # Si no encaja, intenta con formato corto (solo fecha)
            date_obj = datetime.strptime(date_val, "%Y-%m-%d")
    else:
        # Si llega otro tipo (por ejemplo, None o algo raro)
        return None
    
    return {
        "date": date_obj.strftime("%Y-%m-%d"),
        "year": date_obj.year,
        "quarter": math.ceil(date_obj.month / 3),
        "month": date_obj.month,
        "week": date_obj.isocalendar()[1],
        "day": date_obj.day,
        "day_of_week": date_obj.isoweekday()
    }


# --- Función para indexar dimensiones ---
def index_dimension(collection_name):
    collection = db[collection_name]
    actions = []
    for doc in collection.find():
        doc_id = str(doc.pop("_id"))
        index_name = f"dimension_{collection_name.lower()}"
        actions.append({
            "_index": index_name,
            "_id": doc_id,
            "_source": doc
        })
    if actions:
        helpers.bulk(es, actions)
        print(f"Indexed {len(actions)} documents from '{collection_name}'")

# --- Indexar dimensiones básicas ---
for col in dim_collections:
    index_dimension(col)

# --- Crear dimensión tiempo ---
time_index = "northwind_time"
time_ids = set()
actions_time = []

for order in db[orders_collection].find():
    for date_field in ["OrderDate", "ShippedDate"]:
        date_val = order.get(date_field)
        t = build_time_dim(date_val)
        if t:
            t_id = t["date"]
            if t_id not in time_ids:
                actions_time.append({
                    "_index": time_index,
                    "_id": t_id,
                    "_source": t
                })
                time_ids.add(t_id)

if actions_time:
    helpers.bulk(es, actions_time)
    print(f"Indexed {len(actions_time)} documents in 'northwind_time'")

# --- Indexar tabla de hechos Ventas (desglosando Order_details) ---
actions_sales = []


for order in db[orders_collection].find():
    order_id = str(order["_id"])
    customer = db["Customers"].find_one({"CustomerID": order["CustomerID"]})
    employee = db["Employees"].find_one({"EmployeeID": order["EmployeeID"]})
    
    order_details = db[order_details_collection].find({"OrderID": order["OrderID"]})
    
    for item in order_details:
        product = db["Products"].find_one({"ProductID": item["ProductID"]})
        category = db["Categories"].find_one({"CategoryID": product["CategoryID"]})
        supplier = db["Suppliers"].find_one({"SupplierID": product["SupplierID"]})
        
        total = item["Quantity"] * item["UnitPrice"] * (1 - item.get("Discount", 0))
        margen = total - item["Quantity"] * product.get("Cost", 0) if product.get("Cost") else total
        
        sale_doc = {
            "order_id": order_id,
            "quantity": item["Quantity"],
            "unit_price": item["UnitPrice"],
            "discount": item.get("Discount", 0),
            "total": total,
            "margen": margen,
            "customer_id": str(customer["CustomerID"]) if customer else None,
            "employee_id": str(employee["EmployeeID"]) if employee else None,
            "product_id": str(product["ProductID"]) if product else None,
            "category_id": str(category["CategoryID"]) if category else None,
            "supplier_id": str(supplier["SupplierID"]) if supplier else None,
            "time_ordered": build_time_dim(order.get("OrderDate")),
            "time_shipped": build_time_dim(order.get("ShippedDate"))
        }
        
        actions_sales.append({
            "_index": "northwind_sales",
            "_id": f"{order_id}{item['ProductID']}",
            "_source": sale_doc
        })

if actions_sales:
    helpers.bulk(es, actions_sales)
    print(f"Indexed {len(actions_sales)} documents in 'northwind_sales'")

print("¡ETL completo con dimensiones, tabla de hechos Ventas y dimensión tiempo!")
