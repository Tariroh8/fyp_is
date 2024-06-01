from django import template
from django.core.serializers import serialize

register = template.Library()

@register.filter
def geojson_serialize(value):
    return serialize('geojson', value)