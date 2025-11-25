# 📋 Documentación de Endpoints de API AstroCast

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
  "description": "Cielo parcialmente nublado"
}
```

---

## 📌 Resumen Rápido

| Endpoint | Método | Autenticación | Propósito |
|----------|--------|---------------|-----------|
| `/api/auth/token/` | POST | ❌ | Obtener token de acceso |
| `/api/auth/token/refresh/` | POST | ❌ | Refrescar token expirado |
| `/api/accounts/register/` | POST | ❌ | Crear nueva cuenta |
| `/api/accounts/me/` | GET | ✅ | Ver perfil del usuario actual |
| `/api/weather/forecast/` | POST | ✅ | Obtener pronóstico del clima |

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
```
