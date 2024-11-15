#!/bin/bash

# Variables
MONGO_IMAGE_NAME="mongo-image"
MONGO_CONTAINER_NAME="mongo"
NETWORK_NAME="mi_red"
DB_NAME="MiBaseDeDatos"
FLASK_IMAGE_NAME="flask-app"
FLASK_CONTAINER_NAME="flask"

# Crear la red Docker
echo "Creando la red Docker..."
docker network create $NETWORK_NAME

# Ejecutar el contenedor de MongoDB
echo "Levantando el contenedor de MongoDB..."
docker run -d \
    --network $NETWORK_NAME \
    --name $MONGO_CONTAINER_NAME \
    -p 27017:27017 \
    mongo

# Esperar a que MongoDB esté listo
echo "Esperando a que MongoDB esté listo..."
sleep 10  # Ajusta este tiempo si es necesario

# Ejecutar un contenedor temporal para crear la base de datos y las colecciones
echo "Ejecutando un contenedor temporal para crear la base de datos y las colecciones..."
docker run -it --network $NETWORK_NAME --rm mongo /bin/bash -c "
    mongo $DB_NAME --eval 'db.createCollection(\"Usuarios\");'
    mongo $DB_NAME --eval 'db.createCollection(\"Skills\");'
    mongo $DB_NAME --eval 'db.createCollection(\"UsuarioSkills\");'
    mongo $DB_NAME --eval 'db.Usuarios.insert({ ID: 1, Nombre: \"Juan Pérez\" });'
    mongo $DB_NAME --eval 'db.Usuarios.insert({ ID: 2, Nombre: \"María López\" });'
    mongo $DB_NAME --eval 'db.Usuarios.insert({ ID: 3, Nombre: \"Carlos García\" });'
    mongo $DB_NAME --eval 'db.Skills.insert({ ID: 1, Nombre: \"Programación\" });'
    mongo $DB_NAME --eval 'db.Skills.insert({ ID: 2, Nombre: \"Diseño Gráfico\" });'
    mongo $DB_NAME --eval 'db.Skills.insert({ ID: 3, Nombre: \"Gestión de Proyectos\" });'
    mongo $DB_NAME --eval 'db.UsuarioSkills.insert({ ID: 1, ID_Usuario: 1, ID_Skill: 1, Puntuacion: 90 });'
    mongo $DB_NAME --eval 'db.UsuarioSkills.insert({ ID: 2, ID_Usuario: 2, ID_Skill: 2, Puntuacion: 85 });'
    mongo $DB_NAME --eval 'db.UsuarioSkills.insert({ ID: 3, ID_Usuario: 3, ID_Skill: 3, Puntuacion: 95 });'
"

echo "Base de datos y colecciones creadas con éxito."

# Construir la imagen de Flask
echo "Construyendo la imagen de Flask..."
docker build -t $FLASK_IMAGE_NAME -f Dockerfile_flask .

# Ejecutar el contenedor de Flask
echo "Levantando el contenedor de la aplicación Flask..."
docker run -d \
    --network $NETWORK_NAME \
    --name $FLASK_CONTAINER_NAME \
    -e "FLASK_APP=main.py" \
    -e "DATABASE_URL=mongodb://$MONGO_CONTAINER_NAME:27017/$DB_NAME" \
    -p 5000:5000 \
    $FLASK_IMAGE_NAME

echo "Contenedor de la aplicación Flask levantado exitosamente."
