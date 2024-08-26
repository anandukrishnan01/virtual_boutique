# In your app's templatetags/custom_filters.py file
from django import template

register = template.Library()

@register.filter
def make_range(value):
    return range(value)

