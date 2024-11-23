# Imagen base de Python
FROM python:3.10

# Configuración del directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instalación de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000 para la aplicación web
EXPOSE 5000

# Comando de ejecución
CMD ["python", "app.py"]
