from django.template import Library

register = Library()

@register.filter
def subtotal(price, count):
    return '%.2f' %(float(price) * int(count))