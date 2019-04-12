from django import template

register = template.Library()


@register.filter()
def username_capitalize(value):
    return value.capitalize()


