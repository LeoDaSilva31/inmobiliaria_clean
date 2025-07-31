import os
from pathlib import Path
import environ

# Define la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa django-environ para manejar variables del archivo .env
env = environ.Env()
env.read_env(BASE_DIR / '.env')

# Clave secreta de Django (debe estar en el archivo .env)
SECRET_KEY = env('SECRET_KEY')

# Debug activo o no (en producción debe ser False)
DEBUG = env.bool('DEBUG', default=False)

# Lista de hosts permitidos (ejemplo: 127.0.0.1, localhost)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Aplicaciones instaladas en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Para formatear números en templates
    'web_app',  # Tu aplicación principal
]

# Middleware para procesamiento de solicitudes/respuestas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo de configuración de URLs raíz
ROOT_URLCONF = 'django_inmobiliaria.urls'

# Configuración de las plantillas (templates HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ruta de tus plantillas personalizadas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web_app.context_processors.emailjs_keys',  # Si usás EmailJS desde .env
            ],
        },
    },
]

# Configuración WSGI para servidores web
WSGI_APPLICATION = 'django_inmobiliaria.wsgi.application'

# Configuración de base de datos (SQLite por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas para mayor seguridad
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración regional e idioma
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes no subidas)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos multimedia (imágenes subidas por el usuario)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Tipo de campo automático por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Claves de EmailJS, si vas a enviar formularios desde frontend
EMAILJS_PUBLIC_KEY = env("EMAILJS_PUBLIC_KEY")
EMAILJS_SERVICE_ID = env("EMAILJS_SERVICE_ID")
EMAILJS_TEMPLATE_ID = env("EMAILJS_TEMPLATE_ID")
