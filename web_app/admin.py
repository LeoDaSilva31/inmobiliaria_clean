from django.contrib import admin
from .models import Propiedad, PropiedadImagen
from django.contrib.auth.models import Group

# --- Eliminar el modelo Group del panel de administración ---
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# --- Personalización del panel ---
admin.site.site_header = "Administración"
admin.site.site_title = "Administración"
admin.site.index_title = "Administración"

# --- Inline para imágenes ---
class PropiedadImagenInline(admin.TabularInline):
    model = PropiedadImagen
    extra = 1
    fields = ('imagen',)

# --- Administración para Propiedad ---
@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'localidad', 'tipo_operacion', 'precio_usd', 'precio_pesos',
        'is_destacada', 'acepta_mascotas', 'estado_publicacion', 'fecha_actualizacion'
    )
    list_display_links = ('titulo',)
    list_filter = (
        'tipo', 'tipo_operacion', 'localidad', 'is_destacada',
        'acepta_mascotas', 'estado_publicacion'
    )
    search_fields = (
        'titulo', 'descripcion', 'direccion', 'localidad', 'provincia'
    )
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    list_per_page = 25
    ordering = ('-fecha_creacion',)
    inlines = [PropiedadImagenInline]

    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo', 'tipo_operacion')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'localidad', 'provincia')
        }),
        ('Precio', {
            'fields': ('precio_usd', 'precio_pesos')
        }),
        ('Características', {
            'fields': (
                'superficie_total', 'superficie_cubierta',
                'dormitorios', 'banios', 'cocheras'
            )
        }),
        ('Mascotas', {
            'fields': ('acepta_mascotas', 'tipo_mascota_permitida')
        }),
        ('Publicación', {
            'fields': (
                'imagen_principal', 'is_destacada',
                'estado_publicacion', 'fecha_creacion', 'fecha_actualizacion'
            ),
            'classes': ('collapse',)
        }),
    )

    actions = ['publicar_propiedades', 'archivar_propiedades']

    def publicar_propiedades(self, request, queryset):
        updated = queryset.update(estado_publicacion='publicada')
        self.message_user(request, f"{updated} propiedades publicadas.")
    publicar_propiedades.short_description = "Publicar propiedades seleccionadas"

    def archivar_propiedades(self, request, queryset):
        updated = queryset.update(estado_publicacion='borrador')
        self.message_user(request, f"{updated} propiedades marcadas como borrador.")
    archivar_propiedades.short_description = "Archivar propiedades seleccionadas"
