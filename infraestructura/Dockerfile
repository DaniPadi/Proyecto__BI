FROM mcr.microsoft.com/mssql/server:2019-latest
 
# --- Paso 1: Copiar el script SQL ---
USER root
COPY instnwnd.sql /tmp/instnwnd.sql
 
# --- Paso 2: Crear script de inicialización ---
RUN echo '#!/bin/bash\n\
/opt/mssql/bin/sqlservr & \n\
echo "Esperando que SQL Server inicie..." \n\
sleep 25s \n\
echo "Creando base de datos Northwind..." \n\
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd" -C -Q "CREATE DATABASE Northwind" \n\
sleep 3s \n\
echo "Cargando datos..." \n\
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd" -C -d Northwind -i /tmp/instnwnd.sql \n\
wait' > /tmp/init-northwind.sh
 
RUN chmod +x /tmp/init-northwind.sh
 
# --- Paso 3: Cambiar al usuario mssql ---
USER mssql
 
# --- Paso 4: Ejecutar el script al iniciar ---
ENTRYPOINT ["/bin/bash", "/tmp/init-northwind.sh"]


# 1. docker build -t northwind_bd .
# 2. docker run -d --name mssql-northwind -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong!Passw0rd" -p 1433:1433 northwind_bd
# 3. docker logs -f mssql-northwind
# 4. docker exec -it mssql-northwind /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd' -C -d Northwind
# 5. SELECT * FROM Customers