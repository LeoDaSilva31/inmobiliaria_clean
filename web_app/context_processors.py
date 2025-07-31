# web_app/context_processors.py

from django.conf import settings

def emailjs_keys(request):
    """
    Context processor para hacer disponibles las variables de EmailJS en todas las plantillas
    """
    return {
        'EMAILJS_PUBLIC_KEY': settings.EMAILJS_PUBLIC_KEY,
        'EMAILJS_SERVICE_ID': settings.EMAILJS_SERVICE_ID,
        'EMAILJS_TEMPLATE_ID': settings.EMAILJS_TEMPLATE_ID,
    }