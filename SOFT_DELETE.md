# 🗑️ Soft Delete - Guía de Implementación

## ¿Qué es Soft Delete?

Soft Delete es un patrón de diseño donde los registros no se eliminan literalmente de la base de datos, sino que se marcan como eliminados agregando un timestamp `deleted_at`.

### Implementación en AstroCast

Todos los modelos importantes heredan de `SoftDeleteModel`:

- `Location` (Ubicaciones)
- `EventRequest` (Eventos)

## Cómo Usar

### Soft Delete (Marcar como eliminado)

```python
location = Location.objects.get(id=1)
location.delete()  # Soft delete - marca como eliminado
# deleted_at = 2025-11-26 10:30:45.123456+00:00
```

### Ver solo registros NO eliminados (Por defecto)

```python
# Solo devuelve registros donde deleted_at IS NULL
locations = Location.objects.all()
```

### Ver TODOS los registros (incluyendo eliminados)

```python
# Incluye registros donde deleted_at IS NOT NULL
all_locations = Location.objects.with_deleted()
```

### Ver solo registros ELIMINADOS

```python
# Solo devuelve registros donde deleted_at IS NOT NULL
deleted_locations = Location.objects.only_deleted()
```

### Restaurar un registro eliminado

```python
location = Location.objects.only_deleted().get(id=1)
location.restore()  # deleted_at = NULL
```

### Hard Delete (Eliminación literal - NO RECOMENDADO)

```python
location = Location.objects.only_deleted().get(id=1)
location.hard_delete()  # Eliminación literal de la BD
```

## En los Endpoints API

### Eliminar Ubicación

```bash
DELETE /api/weather/locations/{id}/
Authorization: Bearer <token>
```

**Resultado:** Soft delete (marca como eliminado)

### Eliminar Evento

```bash
DELETE /api/events/{id}/
Authorization: Bearer <token>
```

**Resultado:** Soft delete (marca como eliminado)

## Ventajas

✅ **Auditoría:** Mantiene registro de cuándo se eliminó
✅ **Recuperación:** Datos no se pierden, pueden restaurarse
✅ **Integridad:** Evita errores de relaciones rotas
✅ **Compliance:** Cumple con normativas de conservación de datos
✅ **Analytics:** Facilita análisis histórico

## Estructura de la Base de Datos

### Campo `deleted_at`

```sql
ALTER TABLE weather_location ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE events_eventrequest ADD COLUMN deleted_at TIMESTAMP NULL;
```

**Valores:**
- `NULL` = Registro activo/no eliminado
- `2025-11-26 10:30:45` = Eliminado en esa fecha/hora

## Manager Personalizado (`SoftDeleteManager`)

```python
from core.models import SoftDeleteManager

# En tu modelo:
class MyModel(models.Model):
    objects = SoftDeleteManager()
```

**Métodos disponibles:**

| Método | Descripción |
|--------|-------------|
| `.objects.all()` | Solo registros activos |
| `.objects.with_deleted()` | Todos los registros (activos + eliminados) |
| `.objects.only_deleted()` | Solo registros eliminados |

## Ejemplo Completo

```python
# 1. Crear ubicación
location = Location.objects.create(
    user=user,
    name="Oficina",
    latitude=-33.45,
    longitude=-70.66
)

# 2. Ver ubicaciones activas
active = Location.objects.all()  # Incluye location

# 3. Soft delete
location.delete()

# 4. Ver ubicaciones activas (ya no aparece)
active = Location.objects.all()  # NO incluye location

# 5. Ver todas (incluyendo eliminadas)
all_locs = Location.objects.with_deleted()  # Incluye location

# 6. Restaurar
location.restore()
active = Location.objects.all()  # Vuelve a aparecer
```

## Notas Importantes

⚠️ **Backup Regular:** Aunque los datos se conservan, mantén backups regulares
⚠️ **Performance:** Las queries con `with_deleted()` pueden ser más lentas
⚠️ **Limpieza:** Considera políticas de borrado permanente después de X años

---

**Implementado en:** Django 5.2.8 con AstroCast  
**Aplicable a:** Location, EventRequest
