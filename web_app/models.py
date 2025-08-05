# models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from storages.backends.s3boto3 import S3Boto3Storage # <-- Agrega esta línea

s3_storage = S3Boto3Storage() 

class Consulta(models.Model):
    nombre_completo = models.CharField("Nombre Completo", max_length=100)
    email = models.EmailField("Email")
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    mensaje = models.TextField("Mensaje")
    propiedad = models.ForeignKey('Propiedad', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"Consulta de {self.nombre_completo} - {self.email}"



# Modelo principal para las propiedades
class Propiedad(models.Model):
    # Campos de información general
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)

    # Tipos de propiedad y operación
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('terreno', 'Terreno'),
        ('local', 'Local/Oficina'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    TIPO_OPERACION_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]
    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION_CHOICES)

    # Ubicación
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)

    # Precio
    precio_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_pesos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Características
    superficie_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dormitorios = models.IntegerField(null=True, blank=True)
    banios = models.IntegerField(null=True, blank=True)
    cocheras = models.IntegerField(null=True, blank=True)

    # Imagen principal y publicación
    imagen_principal = models.ImageField(
        upload_to='propiedades/',
        storage=s3_storage, # <-- Agrega esto para forzar el uso de S3
        help_text="Imagen destacada de la propiedad. Se sube a S3."
    )
    is_destacada = models.BooleanField(default=False)
    
    ESTADO_PUBLICACION_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('vendida', 'Vendida'),
        ('alquilada', 'Alquilada'),
    ]
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_PUBLICACION_CHOICES, default='borrador')

    # Otros
    acepta_mascotas = models.BooleanField(default=False)
    tipo_mascota_permitida = models.CharField(max_length=100, blank=True, null=True)

    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('propiedad_detail', kwargs={'slug': self.slug})


# Modelo para la galería de imágenes de una propiedad
class PropiedadImagen(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(
        upload_to='propiedades/galeria/',
        storage=s3_storage, # <-- Agrega esto para forzar el uso de S3
    )

    class Meta:
        verbose_name = "Imagen de la Propiedad"
        verbose_name_plural = "Imágenes de la Propiedad"

    def __str__(self):
        return f"Imagen para {self.propiedad.titulo}"