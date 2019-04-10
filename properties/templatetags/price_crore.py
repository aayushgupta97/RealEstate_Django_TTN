from django import template

register = template.Library()


@register.filter()
def convert(value):
    return value/10000000


