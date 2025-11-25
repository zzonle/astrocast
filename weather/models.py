from django.conf import settings
from django.db import models


class Location(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name', 'latitude', 'longitude')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.latitude}, {self.longitude})'


class WeatherCondition(models.Model):
    """
    Catálogo de condiciones: Tormenta, Calor Extremo, Muy Ventoso, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class WeatherQuery(models.Model):
    """
    Registro de cada consulta que hace un usuario al endpoint de forecast.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='weather_queries',
        null=True,
        blank=True,
    )

    latitude = models.FloatField()
    longitude = models.FloatField()
    target_date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    # Lo que llegó en la request (opcional)
    raw_request = models.JSONField(null=True, blank=True)
    # La respuesta limpia que devolviste al cliente (opcional)
    raw_response = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} @ ({self.latitude}, {self.longitude}) {self.target_date}'
