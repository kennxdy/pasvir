from django import template

register = template.Library()


@register.filter(name='phone_number')
def phone_number(number):
    """Convert a 10 character string into (xxx) xxx-xxxx."""
    first = number[0:2]
    second = number[2:7]
    third = number[7:11]
    return '(' + first + ')' + ' ' + second + '-' + third
