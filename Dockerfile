# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar el servidor Gunicorn apuntando al módulo WSGI
CMD ["gunicorn", "biblioteca.wsgi:application", "--bind", "0.0.0.0:8000"]
