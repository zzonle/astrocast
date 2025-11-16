from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    UNIT_CHOICES = [
        ('metric', 'Métrico'),
        ('imperial', 'Imperial'),
    ]

    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'Inglés'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    unit_system = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='metric'
    )
    language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='es'
    )

    def __str__(self):
        return f'Perfil de {self.user.username}'