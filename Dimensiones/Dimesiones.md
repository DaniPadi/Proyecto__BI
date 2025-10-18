## 🧩 Tablas de Dimensiones

### 🕒 DimTiempo
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| TiempoKey | INT | Clave sustituta (PK) |
| Fecha | DATE | Fecha completa |
| Año | INT | Año de la fecha |
| Trimestre | INT | Número de trimestre (1-4) |
| Mes | INT | Número de mes (1-12) |
| NombreMes | VARCHAR(20) | Nombre del mes |
| Día | INT | Día del mes |
| NombreDíaSemana | VARCHAR(20) | Lunes, martes, etc. |
| FinDeSemana | BIT | Indica si es fin de semana |

---

### 👥 DimCliente
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| ClienteKey | INT | Clave sustituta (PK) |
| CustomerID | VARCHAR(10) | ID original del cliente |
| NombreEmpresa | VARCHAR(50) | Nombre de la empresa |
| Contacto | VARCHAR(50) | Persona de contacto |
| CargoContacto | VARCHAR(50) | Cargo del contacto |
| Dirección | VARCHAR(100) | Dirección del cliente |
| Ciudad | VARCHAR(50) | Ciudad |
| Región | VARCHAR(50) | Región o estado |
| CódigoPostal | VARCHAR(20) | Código postal |
| País | VARCHAR(50) | País |
| Teléfono | VARCHAR(30) | Número de teléfono |
| Fax | VARCHAR(30) | Número de fax |

---

### 🧑‍💼 DimEmpleado
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| EmpleadoKey | INT | Clave sustituta (PK) |
| EmployeeID | INT | ID original del empleado |
| NombreCompleto | VARCHAR(100) | Nombre + Apellido |
| Cargo | VARCHAR(50) | Puesto del empleado |
| FechaNacimiento | DATE | Fecha de nacimiento |
| FechaContratación | DATE | Fecha de contratación |
| Ciudad | VARCHAR(50) | Ciudad |
| País | VARCHAR(50) | País |
| JefeID | INT | ID del supervisor |
| TítuloCortesía | VARCHAR(10) | Mr., Ms., etc. |

---

### 📦 DimProducto
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| ProductoKey | INT | Clave sustituta (PK) |
| ProductID | INT | ID original del producto |
| NombreProducto | VARCHAR(100) | Nombre del producto |
| Categoría | VARCHAR(50) | Nombre de la categoría |
| DescripciónCategoría | VARCHAR(200) | Descripción de la categoría |
| Proveedor | VARCHAR(50) | Nombre del proveedor |
| PaísProveedor | VARCHAR(50) | País del proveedor |
| PrecioUnitario | DECIMAL(10,2) | Precio unitario |
| Descontinuado | BIT | Indica si el producto fue descontinuado |

---

### 🏭 DimProveedor
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| ProveedorKey | INT | Clave sustituta (PK) |
| SupplierID | INT | ID original |
| NombreProveedor | VARCHAR(100) | Nombre del proveedor |
| Contacto | VARCHAR(50) | Persona de contacto |
| CargoContacto | VARCHAR(50) | Cargo |
| Dirección | VARCHAR(100) | Dirección |
| Ciudad | VARCHAR(50) | Ciudad |
| País | VARCHAR(50) | País |
| Teléfono | VARCHAR(30) | Teléfono |

---

### 🗂️ DimCategoría
| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| CategoríaKey | INT | Clave sustituta (PK) |
| CategoryID | INT | ID original |
| NombreCategoría | VARCHAR(50) | Nombre |
| Descripción | VARCHAR(200) | Descripción |

---

## 📊 Tabla de Hechos

| Campo | Tipo de dato | Descripción |
|--------|---------------|-------------|
| VentaKey | INT | Clave sustituta (PK) |
| TiempoKey | INT | FK hacia DimTiempo |
| ClienteKey | INT | FK hacia DimCliente |
| EmpleadoKey | INT | FK hacia DimEmpleado |
| ProductoKey | INT | FK hacia DimProducto |
| Cantidad | INT | Unidades vendidas |
| PrecioUnitario | DECIMAL(10,2) | Precio de venta |
| Descuento | DECIMAL(5,2) | Descuento aplicado |
| TotalVenta | DECIMAL(10,2) | Total (Precio × Cantidad × (1 - Descuento)) |

---

## 🔍 Investigación: Elasticsearch y Kibana

### ⚙️ ¿Qué es Elasticsearch?
Elasticsearch es un **motor de búsqueda y análisis de código abierto**, basado en la biblioteca **Apache Lucene**.  
Permite **indexar, consultar y analizar grandes volúmenes de datos** estructurados o no estructurados, en tiempo real.

**Principales características:**
- Altamente **escalable y distribuido**.  
- Utiliza **documentos JSON sin esquema**.  
- Soporta **búsqueda de texto completo** y **agregaciones analíticas**.  
- Se comunica mediante **API RESTful**, lo que lo hace fácil de integrar.

**Usos comunes:**
- Búsqueda avanzada en aplicaciones web.  
- Monitoreo de logs y métricas del sistema.  
- Análisis de datos empresariales en tiempo real.

---

### 📈 ¿Qué es Kibana?
Kibana es una herramienta de **visualización** para los datos almacenados en Elasticsearch.  
Junto con Elasticsearch y Logstash, forma el conocido **ELK Stack (Elastic, Logstash, Kibana)**.

**Funciones principales:**
- Crear **dashboards interactivos** y dinámicos.  
- Representar datos mediante **gráficos, mapas, tablas, histogramas o heatmaps**.  
- Permitir la **monitorización en tiempo real** de métricas clave.  

**Beneficios:**
- 🧩 Código abierto y personalizable.  
- ⚡ Interactivo y en tiempo real.  
- 👁️‍🗨️ Visual e intuitivo.  
- 🔄 Escalable y compatible con Elastic Stack.  

---

## ✅ Entregables de esta sección
- [x] Tablas de dimensiones y hechos completadas.  
- [x] Descripción técnica de Elasticsearch y Kibana.  
- [x] Integración planificada con ETL (Python + Polars).  
- [x] Visualización planificada en Kibana.  

---

