# 📋 Documentación de Endpoints de API AstroCast

Breve descripción
------------------

Este repositorio contiene el backend Django de AstroCast: una API REST para gestionar usuarios, consultas meteorológicas avanzadas y solicitudes de eventos.

Instalación rápida (Windows / PowerShell)
----------------------------------------

1) Sitúate en el directorio del proyecto:

```powershell
cd C:\Users\Admin\.Desarrollo\astrocast
```

2) Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

3) Instala dependencias:

```powershell
pip install -r requirements.txt
```

4) Variables de entorno (usa `.env.example` como plantilla):

```
# Copia .env.example a .env y modifica según tu entorno
SECRET_KEY=your-secret
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
NODE_NASA_API_URL=https://nasa-private.vercel.app/api/probabilities/forecast
ALLOWED_HOSTS=127.0.0.1,localhost
```

5) Migraciones y superusuario:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

Notas sobre dependencias
------------------------

El repo contenía originalmente `requeriments.txt` (con una errata). He añadido `requirements.txt` y `.env.example` para facilitar la puesta en marcha.


## 1️⃣ Autenticación

### 🔐 Obtener Token de Acceso
**Método:** `POST`  
**URL:** `/api/auth/token/`  
**Autenticación:** No requerida

**JSON que acepta:**
```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

**JSON que devuelve:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 🔄 Refrescar Token
**Método:** `POST`  
**URL:** `/api/auth/token/refresh/`  
**Autenticación:** No requerida

**JSON que acepta:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**JSON que devuelve:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2️⃣ Cuentas de Usuario

### 📝 Registrarse
**Método:** `POST`  
**URL:** `/api/accounts/register/`  
**Autenticación:** No requerida

**JSON que acepta:**
```json
{
  "username": "nuevo_usuario",
  "email": "correo@ejemplo.com",
  "password": "contraseña_segura"
}
```

**JSON que devuelve:**
```json
{
  "id": 1,
  "username": "nuevo_usuario",
  "email": "correo@ejemplo.com"
}
```

---

### 👤 Obtener Mi Perfil
**Método:** `GET`  
**URL:** `/api/accounts/me/`  
**Autenticación:** ✅ Requerida (Token Bearer)

**Headers requeridos:**
```
Authorization: Bearer <tu_access_token>
```

**JSON que devuelve:**
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

## 3️⃣ Clima y Pronóstico

### 🌦️ Obtener Pronóstico del Clima
**Método:** `POST`  
**URL:** `/api/weather/forecast/`  
**Autenticación:** ✅ Requerida (Token Bearer)

**Headers requeridos:**
```
Authorization: Bearer <tu_access_token>
Content-Type: application/json
```

**JSON que acepta:**
```json
{
  "location": "-33.45,-70.67",
  "date": "2025-12-25",
  "time": "14:30"
}
```

**Notas sobre los parámetros:**
- `location`: Formato obligatorio "latitud,longitud" (ej: -33.45,-70.67)
- `date`: Formato obligatorio "YYYY-MM-DD"
- `time`: Opcional, formato "HH:MM" (no se utiliza actualmente en el modelo analítico)

**JSON que devuelve:**
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

**⚠️ Importante:** El `weather_query_id` devuelto se usa para vincular este pronóstico con un evento cuando lo crees.

---

## 4️⃣ Eventos

### 📅 Listar y Crear Eventos
**Método:** `GET` / `POST`  
**URL:** `/api/events/`  
**Autenticación:** ✅ Requerida (Token Bearer)

**Headers requeridos:**
```
Authorization: Bearer <tu_access_token>
Content-Type: application/json (para POST)
```

#### GET - Obtener mis eventos
**JSON que devuelve:**
```json
[
  {
    "id": 1,
    "activity": "Desfile de Carnaval",
    "target_date": "2025-12-25",
    "target_time": "14:30",
    "location_id": 5,
    "location_name": "Plaza Mayor",
    "weather_query_id": 42,
    "status": "created",
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
    "created_at": "2025-11-25T11:00:00Z"
  }
]
```

**Filtros disponibles (en la URL):**
- `?status=created` - Filtrar por estado

**Orden:** Los eventos se devuelven ordenados por fecha de creación más reciente.

---

#### POST - Crear un evento nuevo
**JSON que acepta:**
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
- `target_time` (time, opcional, formato HH:MM): Hora del evento

**Campo opcional:**
- `weather_query_id` (integer, opcional): ID de una consulta de clima anterior (obtenido del endpoint `/api/weather/forecast/`)

**Restricciones:**
- La fecha objetivo debe ser futura
- La fecha no puede exceder 7 años en el futuro
- No se permiten eventos duplicados (mismo usuario, ubicación, fecha y actividad)

**JSON que devuelve:**
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
  "created_at": "2025-11-25T12:00:00Z"
}
```

---

## 5️⃣ Ubicaciones (Endpoints implementados)

Ahora el proyecto expone endpoints para que los usuarios gestionen sus ubicaciones guardadas.

- `GET /api/weather/locations/` — Listar todas las ubicaciones del usuario autenticado.
- `POST /api/weather/locations/` — Crear una nueva ubicación (name, city, country, latitude, longitude).
- `GET /api/weather/locations/{id}/` — Obtener los datos de una ubicación propia.
- `PATCH/PUT /api/weather/locations/{id}/` — Actualizar una ubicación propia.
- `DELETE /api/weather/locations/{id}/` — Eliminar una ubicación propia.

Restricciones y notas:
- Todas las rutas requieren autenticación (JWT — Bearer token).
- Cada usuario solo puede ver y modificar sus propias ubicaciones. Intentos de acceder a ubicaciones de otros usuarios devuelven 404.

Ejemplo — Crear una ubicación y usarla:

```bash
# Crear ubicación (con token)
curl -X POST http://localhost:8000/api/weather/locations/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Oficina","city":"Santiago","country":"Chile","latitude":-33.45,"longitude":-70.66}'

# Listar ubicaciones
curl -X GET http://localhost:8000/api/weather/locations/ -H "Authorization: Bearer <ACCESS_TOKEN>"

# Usar una ubicación para crear un evento (ejemplo): suponer location_id es 5
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"activity":"Concierto","target_date":"2026-01-01","location_id":5}'
```

---

## 6️⃣ Resultados de Pronósticos (Próximas Funcionalidades)

> ⚠️ **Nota:** Los endpoints para obtener resultados de pronósticos (ForecastResult) aún no están documentados. Se espera implementar:
> - `GET /api/events/{event_id}/forecast/` - Obtener el pronóstico y análisis de un evento

---

## 📌 Resumen Rápido

| Endpoint | Método | Autenticación | Propósito |
|----------|--------|---------------|-----------|
| `/api/auth/token/` | POST | ❌ | Obtener token de acceso |
| `/api/auth/token/refresh/` | POST | ❌ | Refrescar token expirado |
| `/api/accounts/register/` | POST | ❌ | Crear nueva cuenta |
| `/api/accounts/me/` | GET | ✅ | Ver perfil del usuario actual |
| `/api/weather/forecast/` | POST | ✅ | Obtener pronóstico del clima |
| `/api/weather/locations/` | GET, POST | ✅ | Listar / Crear ubicaciones del usuario |
| `/api/weather/locations/{id}/` | GET, PATCH, DELETE | ✅ | Operaciones sobre ubicación propia |
| `/api/events/` | GET | ✅ | Listar eventos del usuario |
| `/api/events/` | POST | ✅ | Crear un evento nuevo |

---

## 🔧 Ejemplo de Uso Completo

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

# 4. Obtener pronóstico (con token)
curl -X POST http://localhost:8000/api/weather/forecast/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"location":"-33.45,-70.67","date":"2025-12-25","time":"14:30"}'
# Nota: La respuesta incluirá "weather_query_id" que usaremos en el paso 6

# 5. Listar mis eventos
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <access_token>"

# 6. Crear un evento vinculado a la consulta de clima anterior
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
