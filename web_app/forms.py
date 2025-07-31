# web_app/forms.py

from django import forms
from web_app.models import Consulta

# Formulario para enviar una consulta desde el sitio
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre_completo', 'email', 'telefono', 'mensaje']

        # Widgets personalizados para los campos del formulario
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'id': 'id_nombre_completo'  # ID explícito para facilitar en JS o testeo
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu email',
                'id': 'id_email'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu teléfono (opcional)',
                'id': 'id_telefono'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tu mensaje',
                'rows': 5,
                'id': 'id_mensaje'  # Confirmado este id
            }),
        }

        # Etiquetas legibles para los campos del formulario
        labels = {
            'nombre_completo': 'Nombre Completo',
            'email': 'Email',
            'telefono': 'Teléfono',
            'mensaje': 'Mensaje',
        }
