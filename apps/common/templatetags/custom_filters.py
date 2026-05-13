from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='format_price')
def format_price(price):
    return (f'COP {price:,.2f}'
            .replace(',', 'X')
            .replace('.',',')
            .replace('X','.')
    )

