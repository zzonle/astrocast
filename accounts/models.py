from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Preferencias
    unit_system = models.CharField(max_length=10, default='metric', choices=[('metric', 'Métrico'), ('imperial', 'Imperial')])
    language = models.CharField(max_length=10, default='es')
    
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