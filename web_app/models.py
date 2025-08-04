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

    TIPO_OPERACION_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]

    ESTADO_PUBLICACION_CHOICES = [
        ('publicada', 'Publicada'),
        ('borrador', 'Borrador'),
    ]

    TIPO_MASCOTA_CHOICES = [
        ('perros', 'Perros'),
        ('gatos', 'Gatos'),
        ('ambos', 'Perros y Gatos'),
        ('no_especificado', 'No especificado'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION_CHOICES)
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
    tipo_mascota_permitida = models.CharField(max_length=30, choices=TIPO_MASCOTA_CHOICES, default='no_especificado')
    is_destacada = models.BooleanField(default=False)
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_PUBLICACION_CHOICES, default='publicada')
    imagen_principal = models.ImageField(upload_to='propiedades/', null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"


# Imágenes adicionales por propiedad
class PropiedadImagen(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='propiedades/galeria/')

    def __str__(self):
        return f"Imagen de {self.propiedad.titulo}"


# Consultas recibidas
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
