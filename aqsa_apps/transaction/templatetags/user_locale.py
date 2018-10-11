# Author of Aqsa: Yulay Musin
from django import template
from django.utils import formats
register = template.Library()


@register.simple_tag
def short_date_format(language_code):  # request.LANGUAGE_CODE
    return formats.get_format('SHORT_DATE_FORMAT', lang=language_code)


@register.simple_tag
def first_day_of_week(language_code):  # request.LANGUAGE_CODE
    return formats.get_format('FIRST_DAY_OF_WEEK', lang=language_code)
