from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a items de un diccionario en templates"""
    return dictionary.get(key)
