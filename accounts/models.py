from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'English'),
        ('fr', 'Français'),
        ('pt', 'Português'),
    ]
    
    TEMPERATURE_UNIT_CHOICES = [
        ('C', 'Celsius'),
        ('F', 'Fahrenheit'),
        ('K', 'Kelvin'),
    ]
    
    SUBSCRIPTION_CHOICES = [
        ('free', 'Gratuito'),
        ('premium', 'Premium'),
        ('pro', 'Profesional'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Preferencias
    language = models.CharField(max_length=10, default='es', choices=LANGUAGE_CHOICES)
    temperature_unit = models.CharField(max_length=1, default='C', choices=TEMPERATURE_UNIT_CHOICES)
    
    # Perfil personal
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Suscripción
    subscription_plan = models.CharField(max_length=20, default='free', choices=SUBSCRIPTION_CHOICES)
    subscription_expires = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

# --- SEÑALES (Magia automática) ---
# Esto crea el perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()