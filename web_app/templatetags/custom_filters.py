# web_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def formato_miles(valor):
    try:
        return "{:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return valor


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
