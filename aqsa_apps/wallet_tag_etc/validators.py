# Author of Aqsa: Yulay Musin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# User should not be confused in names of wallet_tag_etc.
def two_or_more_spaces(value):
    if '  ' in value:
        raise ValidationError(_('Two or more spaces not allowed'))


# ";" symbol using for put all tags of transaction to one field of CSV.
def reserved_symbol(value):
    if value.find(';') != -1:
        raise ValidationError(_('Please, do not include ";" reserved symbol to name of tag.'))
