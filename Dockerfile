# Imagen base de Python 3.13 (versión slim = liviana)
FROM python:3.13-slim

# No escribir archivos .pyc y no bufferear stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema (build-essential para psycopg2, libpq-dev para PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Recolectar archivos estáticos (whitenoise los sirve desde dentro del contenedor)
RUN python manage.py collectstatic --noinput

# Comando de inicio con Gunicorn (servidor WSGI de producción)
CMD ["gunicorn", "dangerousapi.wsgi:application", "--bind", "0.0.0.0:8000"]