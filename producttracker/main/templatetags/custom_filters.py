from django import template
from django.core.exceptions import ObjectDoesNotExist
from main.models import ProductTracking

register = template.Library()

@register.filter(name='is_tracking')
def is_tracking(product, user):
    try:
        ProductTracking.objects.get(user=user, product=product)
        return True
    
    except ObjectDoesNotExist:
        return False
    
@register.filter(name='equalto')
def equalto(value, arg):
    return value == arg