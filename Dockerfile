# Utiliza una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copia todo el contenido del directorio actual al contenedor
COPY . .

# Expone el puerto 5000 (o el puerto al que se ajuste tu aplicacion)
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]

