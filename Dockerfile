FROM python:3.11

WORKDIR /app

# Instalar herramientas necesarias del sistema (para tensorflow, grpc, psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libglib2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    && apt-get clean

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "biblioteca.wsgi:application", "--bind", "0.0.0.0:8000"]
