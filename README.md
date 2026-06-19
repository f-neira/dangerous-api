# DANGEROUS API

API REST de **Dangerous Band** construida con Django. Proporciona endpoints para gestionar shows, fechas y contenido de la banda.

## Stack

- **Django** — Framework web Python
- **Django REST Framework** — API RESTful
- **PostgreSQL** — Base de datos
- **Docker** — Contenedorización

## Estructura

```
dangerousapi/       # Configuración del proyecto Django
shows/              # App principal
├── models.py       # Modelos de datos
├── views.py        # Vistas y endpoints
├── auth.py         # Autenticación
├── urls.py         # Rutas de la app
├── admin.py        # Panel de administración
├── serializers.py
└── migrations/     # Migraciones de BD
templates/          # Templates HTML
manage.py           # CLI de Django
requirements.txt    # Dependencias Python
Dockerfile          # Build Docker
```

## Variables de entorno

```env
# Autenticación para la API
API_TOKEN=tu_token_secreto
```

## Desarrollo

```bash
# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Migraciones y servidor
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Método | Ruta               | Descripción              |
| ------ | ------------------ | ------------------------ |
| GET    | `/api/shows/`      | Lista de shows           |
| POST   | `/api/shows/`      | Crear show (autenticado) |
| GET    | `/api/shows/{id}/` | Detalle de show          |
| ...    | ...                | ...                      |
