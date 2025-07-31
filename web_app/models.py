from django.db import models

# Modelo principal: Propiedad
class Propiedad(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('ph', 'PH'),
        ('oficina', 'Oficina'),
        ('cochera', 'Cochera'),
        ('local', 'Local'),
        ('terreno', 'Terreno'),
        ('galpon', 'Galpón'),
        ('campo', 'Campo'),
        ('otros', 'Otros'),
    ]

    OPERACION_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_operacion = models.CharField(max_length=20, choices=OPERACION_CHOICES)
    direccion = models.CharField(max_length=200)
    localidad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, default='Buenos Aires')
    precio_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_pesos = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    superficie_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dormitorios = models.IntegerField(null=True, blank=True)
    banios = models.IntegerField(null=True, blank=True)
    cocheras = models.IntegerField(null=True, blank=True)
    acepta_mascotas = models.BooleanField(default=False)
    is_destacada = models.BooleanField(default=False)
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen_principal = models.ImageField(upload_to='propiedades/', null=True, blank=True)

    def __str__(self):
        return self.titulo


# Imagenes adicionales por propiedad
class PropiedadImagen(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='propiedades/galeria/')

    def __str__(self):
        return f"Imagen de {self.propiedad.titulo}"
