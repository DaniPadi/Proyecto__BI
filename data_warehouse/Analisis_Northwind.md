
# Analisis de Tablas – Base de Datos Northwind

## 🧾 1. Tablas Principales de Ventas

### 1.1. Orders
Contiene los pedidos realizados por los clientes.

| Atributo | Descripción |
|-----------|--------------|
| **OrderID** | Identificador único del pedido. |
| **CustomerID** | Identificador del cliente (relación con `Customers`). |
| **EmployeeID** | Identificador del empleado (relación con `Employees`). |
| **OrderDate** | Fecha en la que se realizó el pedido. |
| **RequiredDate** | Fecha solicitada por el cliente para la entrega. |
| **ShippedDate** | Fecha en la que el pedido fue enviado. |
| **ShipVia** | Identificador del transportista (`Shippers`). |
| **Freight** | Costo del envío (flete). |
| **ShipName** | Nombre del destinatario. |
| **ShipAddress** | Dirección de envío. |
| **ShipCity** | Ciudad de destino. |
| **ShipRegion** | Región o estado de destino. |
| **ShipPostalCode** | Código postal de envío. |
| **ShipCountry** | País de destino. |

---

### 1.2. Order_Details
Contiene los detalles de cada producto en los pedidos.

| Atributo | Descripción |
|-----------|-------------|
| **OrderID** | Identificador del pedido (`Orders`). |
| **ProductID** | Identificador del producto (`Products`). |
| **UnitPrice** | Precio unitario al momento de la venta. |
| **Quantity** | Cantidad vendida. |
| **Discount** | Descuento aplicado (0–1). |

> **Clave primaria compuesta:** (OrderID, ProductID)

---

### 1.3. Products
Lista de productos comercializados.

| Atributo | Descripción |
|-----------|-------------|
| **ProductID** | Identificador del producto. |
| **ProductName** | Nombre del producto. |
| **SupplierID** | Identificador del proveedor (`Suppliers`). |
| **CategoryID** | Identificador de la categoría (`Categories`). |
| **QuantityPerUnit** | Descripción del empaque. |
| **UnitPrice** | Precio unitario. |
| **UnitsInStock** | Unidades disponibles. |
| **UnitsOnOrder** | Unidades en pedido. |
| **ReorderLevel** | Nivel de reorden. |
| **Discontinued** | Indica si está descontinuado (0/1). |

---

### 1.4. Categories
Clasificación de productos.

| Atributo | Descripción |
|-----------|-------------|
| **CategoryID** | Identificador de la categoría. |
| **CategoryName** | Nombre de la categoría. |
| **Description** | Descripción general. |
| **Picture** | Imagen representativa (binaria). |

---

### 1.5. Customers
Información de los clientes.

| Atributo | Descripción |
|-----------|-------------|
| **CustomerID** | Identificador del cliente (5 caracteres). |
| **CompanyName** | Nombre de la empresa. |
| **ContactName** | Nombre del contacto. |
| **ContactTitle** | Cargo del contacto. |
| **Address** | Dirección. |
| **City** | Ciudad. |
| **Region** | Región o estado. |
| **PostalCode** | Código postal. |
| **Country** | País. |
| **Phone** | Teléfono. |
| **Fax** | Fax. |

---

### 1.6. Employees
Datos de los empleados (vendedores).

| Atributo | Descripción |
|-----------|-------------|
| **EmployeeID** | Identificador del empleado. |
| **LastName** | Apellido. |
| **FirstName** | Nombre. |
| **Title** | Cargo. |
| **TitleOfCourtesy** | Tratamiento (Mr., Ms., etc.). |
| **BirthDate** | Fecha de nacimiento. |
| **HireDate** | Fecha de contratación. |
| **Address** | Dirección. |
| **City** | Ciudad. |
| **Region** | Región. |
| **PostalCode** | Código postal. |
| **Country** | País. |
| **HomePhone** | Teléfono personal. |
| **Extension** | Extensión telefónica. |
| **Photo** | Fotografía (binaria). |
| **Notes** | Notas. |
| **ReportsTo** | ID del supervisor. |
| **PhotoPath** | Ruta o URL de la imagen. |

---

### 1.7. Shippers
Empresas encargadas de los envíos.

| Atributo | Descripción |
|-----------|-------------|
| **ShipperID** | Identificador del transportista. |
| **CompanyName** | Nombre de la empresa transportadora. |
| **Phone** | Teléfono de contacto. |

---

### 1.8. Suppliers
Proveedores de productos.

| Atributo | Descripción |
|-----------|-------------|
| **SupplierID** | Identificador del proveedor. |
| **CompanyName** | Nombre de la empresa. |
| **ContactName** | Nombre del contacto. |
| **ContactTitle** | Cargo del contacto. |
| **Address** | Dirección. |
| **City** | Ciudad. |
| **Region** | Región. |
| **PostalCode** | Código postal. |
| **Country** | País. |
| **Phone** | Teléfono. |
| **Fax** | Fax. |
| **HomePage** | Página web. |

---

## 🧭 2. Tablas Complementarias

### 2.1. Territories
Define los territorios de operación de los empleados.

| Atributo | Descripción |
|-----------|-------------|
| **TerritoryID** | Identificador del territorio. |
| **TerritoryDescription** | Descripción del territorio. |
| **RegionID** | Identificador de la región (`Region`). |

---

### 2.2. Region
Regiones que agrupan varios territorios.

| Atributo | Descripción |
|-----------|-------------|
| **RegionID** | Identificador de la región. |
| **RegionDescription** | Descripción de la región. |

---

### 2.3. EmployeeTerritories
Relación N:N entre empleados y territorios.

| Atributo | Descripción |
|-----------|-------------|
| **EmployeeID** | Identificador del empleado (`Employees`). |
| **TerritoryID** | Identificador del territorio (`Territories`). |

> **Clave primaria compuesta:** (EmployeeID, TerritoryID)
