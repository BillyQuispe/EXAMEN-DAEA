#!/bin/bash

# Clonar el repositorio
git clone https://github.com/BillyQuispe/EXAMEN-DAEA

# Cambiar al directorio del proyecto
cd EXAMEN-DAEA

# Construir y levantar los contenedores Docker
docker-compose up --build -d
