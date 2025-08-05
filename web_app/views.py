# web_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.db.models import Q

from web_app.models import Propiedad
from .forms import ConsultaForm



def detalle_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    url_imagen = propiedad.url_imagen_principal_firmada(expiracion=300)  # URL válida 5 min
    return render(request, 'detalle_propiedad.html', {'propiedad': propiedad, 'url_imagen': url_imagen})


# --------------------
# VISTA: HOME (Inicio)
# --------------------
def home_view(request):
    propiedades_destacadas = Propiedad.objects.filter(
        is_destacada=True,
        estado_publicacion='publicada'
    )
    # Diccionario con pk -> url firmada
    urls_firmadas = {
        p.pk: p.url_imagen_principal_firmada(expiracion=300)
        for p in propiedades_destacadas
    }
    context = {
        'propiedades_destacadas': propiedades_destacadas,
        'urls_firmadas': urls_firmadas,
        'page_title': 'Inmobiliaria - Inicio',
    }
    return render(request, 'web_app/home.html', context)



# ----------------------------------
# VISTA: LISTADO de PROPIEDADES
# ----------------------------------
def propiedad_list_view(request):
    propiedades = Propiedad.objects.filter(
        estado_publicacion='publicada'
    ).order_by('-fecha_creacion')
    context = {
        'propiedades': propiedades,
        'page_title': 'Listado de Propiedades',
    }
    return render(request, 'web_app/propiedad_list.html', context)


# -------------------------------------
# VISTA: DETALLE de PROPIEDAD + FORM
# -------------------------------------
def propiedad_detail_view(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.propiedad = propiedad
            consulta.save()
            return redirect('web_app:propiedad_detail', pk=propiedad.pk)
    else:
        form = ConsultaForm(initial={'propiedad': propiedad.pk})

    context = {
        'propiedad': propiedad,
        'form': form,
        'page_title': f'{propiedad.titulo} - Detalles',
    }
    return render(request, 'web_app/propiedad_detail.html', context)


# ------------------------
# VISTA: FORMULARIO GENERAL DE CONTACTO
# ------------------------
def contacto_view(request):
    propiedad_id = request.GET.get('propiedad_id')
    propiedad_titulo = request.GET.get('propiedad_titulo')
    propiedad_direccion = request.GET.get('propiedad_direccion')
    propiedad_localidad = request.GET.get('propiedad_localidad')

    initial_data = {}
    if propiedad_id and propiedad_titulo:
        mensaje_inicial = f"\u00a1Hola! Me gustar\u00eda obtener m\u00e1s informaci\u00f3n sobre la propiedad \"{propiedad_titulo}\""
        if propiedad_direccion and propiedad_localidad:
            mensaje_inicial += f" ubicada en {propiedad_direccion}, {propiedad_localidad}."
        elif propiedad_localidad:
            mensaje_inicial += f" ubicada en {propiedad_localidad}."
        mensaje_inicial += " Por favor, cont\u00e1ctenme para conocer los detalles."
        initial_data['mensaje'] = mensaje_inicial

    form = ConsultaForm(initial=initial_data)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            if propiedad_id:
                try:
                    propiedad_asociada = Propiedad.objects.get(pk=propiedad_id)
                    consulta.propiedad = propiedad_asociada
                except Propiedad.DoesNotExist:
                    pass
            consulta.save()
            return redirect(settings.FORMSUBMIT_NEXT)

    context = {
        'form': form,
        'page_title': 'Contacto',
    }
    return render(request, 'web_app/contacto.html', context)


# -----------------------------------------
# VISTA: ENVIO DE FORMULARIO DESDE DETALLE
# -----------------------------------------
def contactar_propiedad_view(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.propiedad = propiedad
            consulta.save()
    return redirect('web_app:propiedad_detail', pk=propiedad.pk)


# ---------------------------
# VISTA: BUSQUEDA DE PROPIEDADES
# ---------------------------
def busqueda_propiedades_view(request):
    # Filtros desde GET
    query = request.GET.get('q')
    tipo_propiedad = request.GET.get('tipo_propiedad')
    tipo_operacion = request.GET.get('tipo_operacion')
    min_precio = request.GET.get('min_precio')
    max_precio = request.GET.get('max_precio')
    currency = request.GET.get('currency', 'ARS')  # Default a ARS
    localidad = request.GET.get('localidad')
    dormitorios = request.GET.get('dormitorios')
    banios = request.GET.get('banios')
    cocheras = request.GET.get('cocheras')
    acepta_mascotas = request.GET.get('acepta_mascotas')
    tipo_mascota_permitida = request.GET.get('tipo_mascota_permitida')
    is_destacada = request.GET.get('is_destacada')

    propiedades = Propiedad.objects.filter(estado_publicacion='publicada')
    active_filters_display = []
    current_get_params = request.GET.copy()

    def generate_remove_url(param_to_remove):
        temp_params = current_get_params.copy()
        if param_to_remove in temp_params:
            del temp_params[param_to_remove]
        return temp_params.urlencode()

    # Filtros básicos
    if query:
        propiedades = propiedades.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(localidad__icontains=query) |
            Q(provincia__icontains=query) |
            Q(amenidades__icontains=query)
        )
        active_filters_display.append({
            'param_name': 'q',
            'display_text': f"Palabra Clave: {query}",
            'remove_url_params': generate_remove_url('q')
        })

    if tipo_propiedad:
        propiedades = propiedades.filter(tipo=tipo_propiedad)
        label = dict(Propiedad.TIPO_CHOICES).get(tipo_propiedad, tipo_propiedad)
        active_filters_display.append({
            'param_name': 'tipo_propiedad',
            'display_text': label.upper(),
            'remove_url_params': generate_remove_url('tipo_propiedad')
        })

    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)
        label = dict(Propiedad.TIPO_OPERACION_CHOICES).get(tipo_operacion, tipo_operacion)
        active_filters_display.append({
            'param_name': 'tipo_operacion',
            'display_text': label.upper(),
            'remove_url_params': generate_remove_url('tipo_operacion')
        })

    # Filtro de precios según moneda
    try:
        if min_precio:
            val_min = float(min_precio)
            if currency == 'USD':
                propiedades = propiedades.filter(precio_usd__gte=val_min)
            else:
                propiedades = propiedades.filter(precio_pesos__gte=val_min)

            active_filters_display.append({
                'param_name': 'min_precio',
                'display_text': f"Precio Desde: {currency} {min_precio}",
                'remove_url_params': generate_remove_url('min_precio')
            })
    except ValueError:
        pass

    try:
        if max_precio:
            val_max = float(max_precio)
            if currency == 'USD':
                propiedades = propiedades.filter(precio_usd__lte=val_max)
            else:
                propiedades = propiedades.filter(precio_pesos__lte=val_max)

            active_filters_display.append({
                'param_name': 'max_precio',
                'display_text': f"Precio Hasta: {currency} {max_precio}",
                'remove_url_params': generate_remove_url('max_precio')
            })
    except ValueError:
        pass

    # Otros filtros de atributos numéricos
    for campo, nombre, label in [
        (localidad, 'localidad', 'Localidad'),
        (dormitorios, 'dormitorios', 'Ambientes'),
        (banios, 'banios', 'Baños'),
        (cocheras, 'cocheras', 'Cocheras')
    ]:
        if campo and campo.isdigit():
            propiedades = propiedades.filter(**{f"{nombre}__gte": int(campo)})
            active_filters_display.append({
                'param_name': nombre,
                'display_text': f"{label}: {campo}",
                'remove_url_params': generate_remove_url(nombre)
            })

    if acepta_mascotas == 'on' or acepta_mascotas == 'True':
        propiedades = propiedades.filter(acepta_mascotas=True)
        active_filters_display.append({
            'param_name': 'acepta_mascotas',
            'display_text': 'Acepta Mascotas',
            'remove_url_params': generate_remove_url('acepta_mascotas')
        })

        if tipo_mascota_permitida and tipo_mascota_permitida != 'no_especificado':
            label = dict(Propiedad.TIPO_MASCOTA_CHOICES).get(tipo_mascota_permitida, tipo_mascota_permitida)
            active_filters_display.append({
                'param_name': 'tipo_mascota_permitida',
                'display_text': f"Tipo Mascota: {label}",
                'remove_url_params': generate_remove_url('tipo_mascota_permitida')
            })

    if is_destacada == 'on' or is_destacada == 'True':
        propiedades = propiedades.filter(is_destacada=True)
        active_filters_display.append({
            'param_name': 'is_destacada',
            'display_text': 'Solo Destacadas',
            'remove_url_params': generate_remove_url('is_destacada')
        })

    propiedades = propiedades.order_by('-fecha_actualizacion')

    context = {
        'propiedades': propiedades,
        'page_title': 'Resultados de Búsqueda',
        'tipo_propiedad_choices': Propiedad.TIPO_CHOICES,
        'tipo_operacion_choices': Propiedad.TIPO_OPERACION_CHOICES,
        'tipo_mascota_choices': Propiedad.TIPO_MASCOTA_CHOICES,
        'selected_tipo_propiedad': tipo_propiedad,
        'selected_tipo_operacion': tipo_operacion,
        'selected_min_precio': min_precio,
        'selected_max_precio': max_precio,
        'selected_currency': currency,
        'selected_localidad': localidad,
        'selected_dormitorios': dormitorios,
        'selected_banios': banios,
        'selected_cocheras': cocheras,
        'selected_acepta_mascotas': 'True' if acepta_mascotas in ['on', 'True'] else None,
        'selected_tipo_mascota_permitida': tipo_mascota_permitida,
        'selected_is_destacada': 'True' if is_destacada in ['on', 'True'] else None,
        'active_filters_display': active_filters_display,
        'request': request,
    }
    return render(request, 'web_app/busqueda.html', context)
