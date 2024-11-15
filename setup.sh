#!/bin/bash

# Variables
NETWORK_NAME="mi_red"
STACK_NAME="voting-app"
COMPOSE_FILE="docker-compose.yml"

# Inicializar Docker Swarm si no está ya inicializado
if [ $(docker info --format '{{.Swarm.LocalNodeState}}') != "active" ]; then
    echo "Inicializando Docker Swarm..."
    docker swarm init
else
    echo "Docker Swarm ya está inicializado."
fi

# Crear la red Docker si no existe
echo "Creando la red Docker si no existe..."
docker network ls | grep -q $NETWORK_NAME || docker network create $NETWORK_NAME

# Verificar si el archivo docker-compose.yml existe
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "El archivo docker-compose.yml no se encuentra. Asegúrate de tenerlo en el directorio correcto."
    exit 1
fi

# Desplegar la pila (stack) usando Docker Compose
echo "Desplegando la pila en Docker Swarm..."
docker stack deploy -c $COMPOSE_FILE $STACK_NAME

# Escalar servicios según sea necesario (por ejemplo, Flask a 3 réplicas)
echo "Escalando el servicio Flask..."
docker service scale ${STACK_NAME}_flask=3

# Comprobamos el estado de los servicios
echo "Comprobando el estado de los servicios..."
docker service ls

echo "¡La configuración y el despliegue en Docker Swarm se han completado con éxito!"
