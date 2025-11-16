from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from weather.models import Location, WeatherCondition


class EventRequest(models.Model):
    STATUS_CHOICES = [
        ('created', 'Creado'),
        ('processed', 'Procesado'),
        ('cancelled', 'Cancelado'),
        ('deleted', 'Eliminado'),   # para "borrado lógico" si lo necesitas
        ('error', 'Error'),         # útil cuando falle NASA/modelo
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_requests'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='event_requests'
    )
    target_date = models.DateField()
    # Hora es opcional / irrelevante
    target_time = models.TimeField(blank=True, null=True)

    activity = models.CharField(
        max_length=200,
        help_text='Ej: desfile, concierto, partido, etc.'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Evitar duplicar la misma consulta exacta por usuario
        unique_together = ('user', 'location', 'target_date', 'activity')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.activity} en {self.location} el {self.target_date}'

    def clean(self):
        from django.core.exceptions import ValidationError

        # No permitir fechas fuera del rango del modelo (1990–2020 de entrenamiento,
        # y hasta ~6–7 años hacia adelante desde "hoy").
        if self.target_date < timezone.now().date():
            raise ValidationError('La fecha objetivo debe ser futura.')

        # Por ejemplo: limitar a 7 años desde hoy (ajustable)
        max_allowed = timezone.now().date().replace(year=timezone.now().year + 7)
        if self.target_date > max_allowed:
            raise ValidationError('La fecha objetivo no puede exceder 7 años hacia adelante.')

class ForecastResult(models.Model):
    event_request = models.OneToOneField(
        EventRequest,
        on_delete=models.CASCADE,
        related_name='forecast'
    )

    # Probabilidad de lluvia (%)
    rain_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text='Probabilidad de lluvia en porcentaje.'
    )

    # Probabilidad global de "condiciones adversas" si quieres un resumen general
    adverse_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text='Probabilidad global de condiciones adversas (%).'
    )

    # Detalle por tipo (Muy Caluroso, Muy Frío, etc.) guardado como JSON
    adverse_details = models.JSONField(
        blank=True,
        null=True,
        help_text='Detalle de probabilidades por condición adversa.'
    )

    LABEL_CHOICES = [
        ('favorable', 'Favorable'),
        ('unfavorable', 'No favorable'),
    ]
    label = models.CharField(
        max_length=20,
        choices=LABEL_CHOICES
    )

    summary = models.TextField(blank=True)

    # Tags de riesgo principales
    conditions = models.ManyToManyField(
        WeatherCondition,
        related_name='forecasts',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pronóstico para {self.event_request} ({self.label})'

class Report(models.Model):
    """
    Metadatos de informe generado (PDF/Excel).
    Aunque el modelo permita varios, en tu flujo solo generarás uno por EventRequest.
    """
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
    ]

    event_request = models.ForeignKey(
        EventRequest,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    file = models.FileField(upload_to='reports/')
    file_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default='pdf'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(
        max_length=64,
        blank=True,
        help_text='Hash opcional para verificar integridad.'
    )

    def __str__(self):
        return f'Reporte {self.file.name} ({self.file_format})'

class DataSource(models.Model):
    """
    Traza de las consultas a NASA y/o a tu modelo estadístico.
    """
    SOURCE_CHOICES = [
        ('nasa', 'NASA'),
        ('model', 'Modelo Estadístico'),
    ]

    forecast = models.ForeignKey(
        ForecastResult,
        on_delete=models.CASCADE,
        related_name='data_sources'
    )
    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES
    )

    endpoint = models.URLField(max_length=300)
    # parámetros usados en la llamada (lat, lon, targetDate, etc.)
    request_params = models.JSONField()

    response_status = models.IntegerField(
        null=True,
        blank=True,
        help_text='Código HTTP de respuesta (si aplica).'
    )
    response_time_ms = models.IntegerField(
        null=True,
        blank=True,
        help_text='Tiempo de respuesta en milisegundos.'
    )

    payload = models.JSONField(
        null=True,
        blank=True,
        help_text='Respuesta cruda (JSON) para auditoría.'
    )

    error_message = models.TextField(
        blank=True,
        help_text='Detalle en caso de error.'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'DataSource {self.source_type} para {self.forecast_id}'


