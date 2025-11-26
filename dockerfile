# Usamos una imagen ligera de Python oficial
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo en el servidor
WORKDIR /app

# Instalamos dependencias básicas del sistema (útil para psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiamos los requisitos e instalamos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos todo el código del proyecto
COPY . /app/

# Exponemos el puerto
EXPOSE 8000

# Comando para iniciar (incluye migraciones y collectstatic)
# Usamos "sh -c" para poder encadenar comandos
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn astrocast.wsgi:application --bind 0.0.0.0:8000"]