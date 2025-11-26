from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager personalizado que excluye objetos eliminados"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def with_deleted(self):
        """Incluir objetos eliminados"""
        return super().get_queryset()
    
    def only_deleted(self):
        """Solo objetos eliminados"""
        return super().get_queryset().filter(deleted_at__isnull=False)


class SoftDeleteModel(models.Model):
    """Modelo base para implementar soft delete"""
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
    
    def delete(self, *args, **kwargs):
        """Soft delete - marcar como eliminado sin borrar del DB"""
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self):
        """Hard delete - eliminación literal de la DB"""
        super().delete()
    
    def restore(self):
        """Restaurar un objeto eliminado"""
        self.deleted_at = None
        self.save()
    
    def is_deleted(self):
        """Verificar si está eliminado"""
        return self.deleted_at is not None
