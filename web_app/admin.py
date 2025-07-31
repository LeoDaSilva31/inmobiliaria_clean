# admin.py organizado y comentado

from django.contrib import admin
from django.utils.html import format_html
from .models import Propiedad, PropiedadImagen

# --- Personalización del sitio admin ---
admin.site.site_header = "Administración"

# --- Imagenes Inline para la Propiedad ---
class PropiedadImagenInline(admin.TabularInline):
    model = PropiedadImagen
    extra = 1
    fields = ('imagen', 'descripcion_corta')


# --- Configuración del modelo Propiedad en el admin ---
@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    # Campos visibles en la lista
    list_display = (
        'titulo', 'localidad', 'tipo_operacion', 'precio_usd', 'precio_pesos',
        'is_destacada', 'acepta_mascotas', 'estado_publicacion', 'fecha_actualizacion'
    )
    list_display_links = ('titulo',)

    # Filtros laterales
    list_filter = (
        'tipo', 'tipo_operacion', 'localidad', 'is_destacada', 'acepta_mascotas',
        'estado_publicacion', 'fecha_creacion', 'fecha_actualizacion', 'tipo_mascota_permitida'
    )

    # Campos buscables
    search_fields = (
        'titulo', 'descripcion', 'direccion', 'localidad', 'provincia', 'amenidades'
    )

    # Orden y paginación
    list_per_page = 25
    ordering = ('-fecha_creacion',)

    # Campos de solo lectura
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    # Agrupación de campos por secciones
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo', 'tipo_operacion'),
            'description': 'Información fundamental de la propiedad.'
        }),
        ('Detalles de Precio', {
            'fields': ('precio_usd', 'precio_pesos'),
            'description': 'Define los precios de venta o alquiler. Al menos uno debe ser completado.'
        }),
        ('Ubicación', {
            'fields': ('direccion', 'localidad', 'provincia', 'pais'),
            'description': 'Ubicación física de la propiedad.'
        }),
        ('Características', {
            'fields': ('metros_cuadrados_total', 'metros_cuadrados_cubierta', 'dormitorios', 'banios', 'cocheras', 'antiguedad', 'amenidades'),
            'description': 'Especificaciones y comodidades de la propiedad.'
        }),
        ('Mascotas', {
            'fields': ('acepta_mascotas', 'tipo_mascota_permitida'),
            'description': 'Configuración de si la propiedad es amigable con mascotas y sus restricciones.'
        }),
        ('Gestión y Publicación', {
            'fields': ('imagen_principal', 'is_destacada', 'estado_publicacion', 'fecha_creacion', 'fecha_actualizacion'),
            'description': 'Control de la visibilidad y estado de la propiedad.',
            'classes': ('collapse',),
        }),
    )

    # Inlines
    inlines = [PropiedadImagenInline]

    # Acciones personalizadas
    actions = ['make_destacada', 'make_not_destacada', 'publish_property', 'archive_property']

    def make_destacada(self, request, queryset):
        updated = queryset.update(is_destacada=True)
        self.message_user(request, f'{updated} propiedades marcadas como destacadas.', level='success')
    make_destacada.short_description = "Marcar propiedades seleccionadas como destacadas"

    def make_not_destacada(self, request, queryset):
        updated = queryset.update(is_destacada=False)
        self.message_user(request, f'{updated} propiedades desmarcadas como destacadas.', level='warning')
    make_not_destacada.short_description = "Desmarcar propiedades seleccionadas como destacadas"

    def publish_property(self, request, queryset):
        updated = queryset.update(estado_publicacion='publicada')
        self.message_user(request, f'{updated} propiedades publicadas.', level='success')
    publish_property.short_description = "Publicar propiedades seleccionadas"

    def archive_property(self, request, queryset):
        updated = queryset.update(estado_status='archivada')  # Asegurarse que 'estado_status' existe
        self.message_user(request, f'{updated} propiedades archivadas.', level='warning')
    archive_property.short_description = "Archivar propiedades seleccionadas"


# --- Desregistrar modelos innecesarios del admin ---
try:
    from django.contrib.auth.models import Group, User
    admin.site.unregister(Group)
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
