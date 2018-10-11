# Author of Aqsa: Yulay Musin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


IMPORT_FILE_MAX_SIZE = ('1000 Kb', 1000 * 1024)


# Model field validator.
def file_size(value):
    if value.size > IMPORT_FILE_MAX_SIZE[1]:
        raise ValidationError(_('Please, upload smaller file. Size of uploading file should be less than {0}'.
                                format(IMPORT_FILE_MAX_SIZE[0])))


# Model field validator.
def file_extension(value):
    extension = value.name.split('.')[-1]
    if extension != 'csv' and extension != 'txt' and extension != 'zip':
        raise ValidationError(_('Please, upload ".txt" or ".csv" or ".zip" file.'))


# Form field validator.
def plus_minus_symbol(value):
    if value != '+' and value != '-':
        raise ValidationError(_('Only "+" and "-" symbols can be.'))
