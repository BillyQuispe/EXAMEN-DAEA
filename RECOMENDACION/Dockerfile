# Usa la imagen oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará la API (5000)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
