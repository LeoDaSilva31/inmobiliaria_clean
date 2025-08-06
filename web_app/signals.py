# web_app/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Propiedad, PropiedadImagen

# Eliminar imagen de galería del bucket al borrar la instancia
@receiver(post_delete, sender=PropiedadImagen)
def eliminar_imagen_galeria_s3(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)

# Eliminar imagen principal del bucket al borrar la propiedad
@receiver(post_delete, sender=Propiedad)
def eliminar_imagen_principal_s3(sender, instance, **kwargs):
    if instance.imagen_principal:
        instance.imagen_principal.delete(save=False)
