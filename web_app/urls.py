# web_app/urls.py

from django.urls import path
from . import views

# Nombre de espacio para la app (importante para usar {% url %} en templates)
app_name = 'web_app'

urlpatterns = [
    # Página de inicio
    path('', views.home_view, name='home'),

    # Listado de propiedades
    path('propiedades/', views.propiedad_list_view, name='propiedad_list'),

    # Detalle de una propiedad específica
    path('propiedad/<int:pk>/', views.propiedad_detail_view, name='propiedad_detail'),

    # Formulario de contacto general
    path('contacto/', views.contacto_view, name='contacto'),

    # Búsqueda de propiedades
    path('busqueda/', views.busqueda_propiedades_view, name='busqueda'),

    # Formulario de contacto específico para una propiedad
    path('propiedad/<int:pk>/contactar/', views.contactar_propiedad_view, name='contactar_propiedad'),
]
