# Author of Aqsa: Yulay Musin
from django import template
register = template.Library()


@register.filter(name='model_property')
def model_property(field_name, query_row_field):
    return eval('query_row_field.' + field_name)
