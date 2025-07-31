# django_inmobiliaria/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # URLs de la app principal (web_app), con espacio de nombres 'web_app'
    path('', include(('web_app.urls', 'web_app'), namespace='web_app')),
]

# Manejo de archivos multimedia durante el desarrollo
# Esto solo funciona si DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
