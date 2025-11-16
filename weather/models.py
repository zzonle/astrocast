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
        # Evita que un mismo usuario registre exactamente la misma ubicación varias veces
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