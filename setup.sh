#!/bin/bash

# Variables
IMAGE_NAME="sqlserver-image"
CONTAINER_NAME="sqlserver"
NETWORK_NAME="mi_red"
DB_NAME="MiBaseDeDatos"
SA_PASSWORD="StrongPassword123"
FLASK_IMAGE_NAME="flask-app"
FLASK_CONTAINER_NAME="flask"

# Crear la red Docker
echo "Creando la red Docker..."
docker network create $NETWORK_NAME

# Construir la imagen de SQL Server
echo "Construyendo la imagen de SQL Server..."
docker build -t $IMAGE_NAME .

# Ejecutar el contenedor de SQL Server
echo "Levantando el contenedor de SQL Server..."
docker run -d \
    --network $NETWORK_NAME \
    --name $CONTAINER_NAME \
    -e "ACCEPT_EULA=Y" \
    -e "MSSQL_SA_PASSWORD=$SA_PASSWORD" \
    -e "MSSQL_PID=Express" \
    -p 1433:1433 \
    $IMAGE_NAME

# Esperar a que SQL Server esté listo
echo "Esperando a que SQL Server esté listo..."
sleep 30  # Ajusta este tiempo si es necesario

# Ejecutar un contenedor temporal para crear la base de datos y las tablas
echo "Ejecutando un contenedor temporal para crear la base de datos y las tablas..."
docker run -it --network $NETWORK_NAME --rm mcr.microsoft.com/mssql-tools /bin/bash -c "
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d master -Q \"CREATE DATABASE $DB_NAME;\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"CREATE TABLE Usuarios (ID INT PRIMARY KEY, Nombre NVARCHAR(100));\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"CREATE TABLE Skills (ID INT PRIMARY KEY, Nombre NVARCHAR(100));\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"CREATE TABLE UsuarioSkills (ID INT PRIMARY KEY, ID_Usuario INT, ID_Skill INT, Puntuacion INT, FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID), FOREIGN KEY (ID_Skill) REFERENCES Skills(ID));\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Usuarios (ID, Nombre) VALUES (1, 'Juan Pérez');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Usuarios (ID, Nombre) VALUES (2, 'María López');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Usuarios (ID, Nombre) VALUES (3, 'Carlos García');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Skills (ID, Nombre) VALUES (1, 'Programación');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Skills (ID, Nombre) VALUES (2, 'Diseño Gráfico');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO Skills (ID, Nombre) VALUES (3, 'Gestión de Proyectos');\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO UsuarioSkills (ID, ID_Usuario, ID_Skill, Puntuacion) VALUES (1, 1, 1, 90);\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO UsuarioSkills (ID, ID_Usuario, ID_Skill, Puntuacion) VALUES (2, 2, 2, 85);\"
    sqlcmd -S $CONTAINER_NAME -U sa -P $SA_PASSWORD -d $DB_NAME -Q \"INSERT INTO UsuarioSkills (ID, ID_Usuario, ID_Skill, Puntuacion) VALUES (3, 3, 3, 95);\"
"

echo "Base de datos y tablas creadas con éxito."

# Construir la imagen de Flask
echo "Construyendo la imagen de Flask..."
docker build -t $FLASK_IMAGE_NAME -f Dockerfile_flask .

# Ejecutar el contenedor de Flask
echo "Levantando el contenedor de la aplicación Flask..."
docker run -d \
    --network $NETWORK_NAME \
    --name $FLASK_CONTAINER_NAME \
    -e "FLASK_APP=main.py" \
    -e "DATABASE_URL=DRIVER={ODBC Driver 17 for SQL Server};SERVER=$CONTAINER_NAME;DATABASE=$DB_NAME;UID=sa;PWD=$SA_PASSWORD" \
    -p 5000:5000 \
    $FLASK_IMAGE_NAME

echo "Contenedor de la aplicación Flask levantado exitosamente."
