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