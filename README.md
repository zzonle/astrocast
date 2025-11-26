# 📋 Documentación de Endpoints de API AstroCast

## Breve descripción

Este repositorio contiene el backend Django de AstroCast: una API REST para gestionar usuarios, consultas meteorológicas avanzadas y solicitudes de eventos.

## Instalación rápida (Windows / PowerShell)

1. Sitúate en el directorio del proyecto:

```powershell
cd C:\Users\Admin\.Desarrollo\astrocast
```

2. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

3. Instala dependencias:

```powershell
pip install -r requirements.txt
```

4. Configura variables de entorno (usa `.env.example` como plantilla):

```
SECRET_KEY=your-secret
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
NODE_NASA_API_URL=https://nasa-private.vercel.app/api/probabilities/forecast
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=
```

**CORS:** 
- Si `CORS_ALLOWED_ORIGINS` está vacío → permite cualquier origen (desarrollo/testing)
- Si tiene valores específicos → solo esos orígenes pueden acceder

Ejemplo para producción con dominio:
```
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

5. Ejecuta migraciones y crea superusuario:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

### Nota sobre dependencias

El repositorio contenía originalmente `requeriments.txt` (con una errata). Se ha añadido `requirements.txt` y `.env.example` para facilitar la puesta en marcha.

---

## 1. Autenticación

### Obtener Token de Acceso

**Método:** `POST`  
**URL:** `/api/auth/token/`  
**Autenticación:** No requerida

Solicitud:

```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

Respuesta:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Refrescar Token

**Método:** `POST`  
**URL:** `/api/auth/token/refresh/`  
**Autenticación:** No requerida

Solicitud:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Respuesta:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2. Cuentas de Usuario

### Registrarse

**Método:** `POST`  
**URL:** `/api/accounts/register/`  
**Autenticación:** No requerida

Solicitud:

```json
{
  "username": "nuevo_usuario",
  "email": "correo@ejemplo.com",
  "password": "contraseña_segura"
}
```

Respuesta:

```json
{
  "id": 1,
  "username": "nuevo_usuario",
  "email": "correo@ejemplo.com"
}
```

### Obtener Mi Perfil

**Método:** `GET`  
**URL:** `/api/accounts/me/`  
**Autenticación:** Requerida (Token Bearer)

Headers requeridos:

```
Authorization: Bearer <tu_access_token>
```

Respuesta:

```json
{
  "id": 1,
  "username": "tu_usuario",
  "email": "correo@ejemplo.com",
  "profile": {
    "unit_system": "metric",
    "language": "es"
  }
}
```

---

## 3. Clima y Pronóstico

### Obtener Pronóstico del Clima

**Método:** `POST`  
**URL:** `/api/weather/forecast/`  
**Autenticación:** Requerida (Token Bearer)

Headers requeridos:

```
Authorization: Bearer <tu_access_token>
Content-Type: application/json
```

Solicitud:

```json
{
  "location": "-33.45,-70.67",
  "date": "2025-12-25",
  "time": "14:30"
}
```

**Parámetros:**

- `location`: Formato obligatorio "latitud,longitud" (ejemplo: -33.45,-70.67)
- `date`: Formato obligatorio YYYY-MM-DD
- `time`: Opcional, formato HH:MM (no se utiliza actualmente en el modelo analítico)

Respuesta:

```json
{
  "latitude": -33.45,
  "longitude": -70.67,
  "date": "2025-12-25",
  "time": "14:30",
  "temperature": 22.5,
  "humidity": 65,
  "wind_speed": 12.3,
  "cloud_cover": 30,
  "visibility": 10,
  "description": "Cielo parcialmente nublado",
  "weather_query_id": 42
}
```

**Importante:** El `weather_query_id` devuelto se usa para vincular este pronóstico con un evento.

---

## 4. Eventos

### Listar Eventos

**Método:** `GET`  
**URL:** `/api/events/`  
**Autenticación:** Requerida (Token Bearer)

Headers requeridos:

```
Authorization: Bearer <tu_access_token>
```

Respuesta:

```json
[
  {
    "id": 1,
    "activity": "Desfile de Carnaval",
    "target_date": "2025-12-25",
    "target_time": "14:30",
    "location_id": 5,
    "location_name": "Plaza Mayor",
    "weather_query_id": 3,
    "status": "created",
    "created_by": "user1",
    "created_by_email": "user1@example.com",
    "created_at": "2025-11-25T10:30:00Z"
  },
  {
    "id": 2,
    "activity": "Concierto al aire libre",
    "target_date": "2026-01-15",
    "target_time": "20:00",
    "location_id": 6,
    "location_name": "Parque Central",
    "weather_query_id": null,
    "status": "created",
    "created_by": "user1",
    "created_by_email": "user1@example.com",
    "created_at": "2025-11-25T11:00:00Z"
  }
]
```

**Campos retornados:**

- `id`: ID único del evento
- `activity`: Nombre/descripción del evento
- `target_date`: Fecha del evento
- `target_time`: Hora del evento (si aplica)
- `location_id`: ID de la ubicación
- `location_name`: Nombre de la ubicación
- `weather_query_id`: ID de la consulta climática vinculada (null si no hay vínculo)
- `status`: Estado del evento
- `created_by`: Usuario que creó el evento
- `created_by_email`: Email del usuario que creó el evento
- `created_at`: Fecha y hora de creación

**Filtros disponibles:**

- `?status=created` - Filtrar por estado

**Orden:** Los eventos se devuelven ordenados por fecha de creación (más recientes primero).

### Crear Evento

**Método:** `POST`  
**URL:** `/api/events/`  
**Autenticación:** Requerida (Token Bearer)

Headers requeridos:

```
Authorization: Bearer <tu_access_token>
Content-Type: application/json
```

Solicitud:

```json
{
  "activity": "Concierto al aire libre",
  "target_date": "2026-01-15",
  "target_time": "20:00",
  "location_id": 6,
  "weather_query_id": 42
}
```

**Campos requeridos:**

- `activity` (string, máx 200 caracteres): Nombre o descripción del evento
- `target_date` (date, formato YYYY-MM-DD): Fecha futura del evento
- `location_id` (integer): ID de una ubicación existente del usuario

**Campos opcionales:**

- `target_time` (time, formato HH:MM): Hora del evento
- `weather_query_id` (integer): ID de una consulta de clima anterior

**Restricciones:**

- La fecha objetivo debe ser futura
- La fecha no puede exceder 7 años en el futuro
- No se permiten eventos duplicados (mismo usuario, ubicación, fecha y actividad)

Respuesta:

```json
{
  "id": 3,
  "activity": "Concierto al aire libre",
  "target_date": "2026-01-15",
  "target_time": "20:00",
  "location_id": 6,
  "location_name": "Parque Central",
  "weather_query_id": 42,
  "status": "created",
  "created_by": "user1",
  "created_by_email": "user1@example.com",
  "created_at": "2025-11-25T12:00:00Z"
}
```

**Nota:** El campo `weather_query_id` se devuelve tanto en la creación como en la consulta de eventos, permitiendo rastrear la consulta climática que generó cada evento.

---

## 5. Ubicaciones

### Listar Ubicaciones

**Método:** `GET`  
**URL:** `/api/weather/locations/`  
**Autenticación:** Requerida (Token Bearer)

### Crear Ubicación

**Método:** `POST`  
**URL:** `/api/weather/locations/`  
**Autenticación:** Requerida (Token Bearer)

Solicitud:

```json
{
  "name": "Oficina",
  "city": "Santiago",
  "country": "Chile",
  "latitude": -33.45,
  "longitude": -70.66
}
```

### Obtener Ubicación

**Método:** `GET`  
**URL:** `/api/weather/locations/{id}/`  
**Autenticación:** Requerida (Token Bearer)

### Actualizar Ubicación

**Método:** `PATCH` o `PUT`  
**URL:** `/api/weather/locations/{id}/`  
**Autenticación:** Requerida (Token Bearer)

### Eliminar Ubicación

**Método:** `DELETE`  
**URL:** `/api/weather/locations/{id}/`  
**Autenticación:** Requerida (Token Bearer)

**Restricciones:**

- Todas las rutas requieren autenticación (JWT — Token Bearer)
- Cada usuario solo puede ver y modificar sus propias ubicaciones
- Intentos de acceder a ubicaciones de otros usuarios devuelven error 404

---

## 6. Resultados de Pronósticos

> **Nota:** Los endpoints para obtener resultados de pronósticos (ForecastResult) aún no están documentados. Se espera implementar:
> - `GET /api/events/{event_id}/forecast/` - Obtener el pronóstico y análisis de un evento

---

## Resumen Rápido

| Endpoint | Método | Autenticación | Propósito |
|----------|--------|---|-----------|
| `/api/auth/token/` | POST | No | Obtener token de acceso |
| `/api/auth/token/refresh/` | POST | No | Refrescar token expirado |
| `/api/accounts/register/` | POST | No | Crear nueva cuenta |
| `/api/accounts/me/` | GET | Sí | Ver perfil del usuario actual |
| `/api/weather/forecast/` | POST | Sí | Obtener pronóstico del clima |
| `/api/weather/locations/` | GET, POST | Sí | Listar y crear ubicaciones |
| `/api/weather/locations/{id}/` | GET, PATCH, DELETE | Sí | Operaciones sobre ubicación propia |
| `/api/events/` | GET, POST | Sí | Listar y crear eventos |

---

## Ejemplo de Uso Completo

```bash
# 1. Registrarse
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user@example.com","password":"pass123"}'

# 2. Obtener token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'

# 3. Obtener perfil (con token)
curl -X GET http://localhost:8000/api/accounts/me/ \
  -H "Authorization: Bearer <access_token>"

# 4. Crear una ubicación
curl -X POST http://localhost:8000/api/weather/locations/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Oficina","city":"Santiago","country":"Chile","latitude":-33.45,"longitude":-70.66}'

# 5. Obtener pronóstico
curl -X POST http://localhost:8000/api/weather/forecast/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"location":"-33.45,-70.67","date":"2025-12-25","time":"14:30"}'

# 6. Listar eventos
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <access_token>"

# 7. Crear un evento vinculado a la consulta de clima
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "Concierto al aire libre",
    "target_date": "2025-12-25",
    "target_time": "20:00",
    "location_id": 1,
    "weather_query_id": 42
  }'
```
