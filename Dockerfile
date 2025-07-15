FROM python:3.11-slim

WORKDIR /app

# Instalar librerías del sistema necesarias para paquetes complicados
RUN apt-get update && apt-get install -y \
    build-essential \
    libdbus-1-dev \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "biblioteca.wsgi:application", "--bind", "0.0.0.0:8000"]
