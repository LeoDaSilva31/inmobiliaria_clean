import os
import django
import random
from decimal import Decimal
from faker import Faker

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_inmobiliaria.settings")


  # reemplazá con el nombre real
django.setup()

from web_app.models import Propiedad
  # ajustá "app" con el nombre de tu app

fake = Faker('es_AR')  # localización argentina

TIPO_CHOICES = [choice[0] for choice in Propiedad.TIPO_CHOICES]
TIPO_OPERACION_CHOICES = [choice[0] for choice in Propiedad.TIPO_OPERACION_CHOICES]
ESTADO_PUBLICACION_CHOICES = [choice[0] for choice in Propiedad.ESTADO_PUBLICACION_CHOICES]
TIPO_MASCOTA_CHOICES = [choice[0] for choice in Propiedad.TIPO_MASCOTA_CHOICES]

def crear_propiedades(cantidad=20):
    for _ in range(cantidad):
        precio_usd = Decimal(random.randint(30000, 500000))
        precio_pesos = precio_usd * Decimal('1000')  # valor ficticio

        propiedad = Propiedad.objects.create(
            titulo=fake.sentence(nb_words=4),
            descripcion=fake.paragraph(nb_sentences=5),
            tipo=random.choice(TIPO_CHOICES),
            tipo_operacion=random.choice(TIPO_OPERACION_CHOICES),
            direccion=fake.street_address(),
            localidad=fake.city(),
            provincia="Buenos Aires",
            precio_usd=precio_usd,
            precio_pesos=precio_pesos,
            superficie_total=Decimal(random.randint(40, 300)),
            dormitorios=random.randint(0, 5),
            banios=random.randint(1, 3),
            cocheras=random.randint(0, 2),
            acepta_mascotas=random.choice([True, False]),
            tipo_mascota_permitida=random.choice(TIPO_MASCOTA_CHOICES),
            is_destacada=random.choice([True, False]),
            estado_publicacion=random.choice(ESTADO_PUBLICACION_CHOICES),
        )

        print(f"Propiedad creada: {propiedad.titulo}")

if __name__ == "__main__":
    crear_propiedades(30)
