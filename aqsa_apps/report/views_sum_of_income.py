# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from django.utils.translation import gettext as _
from . import forms as f


class List(vxmx.ListReportMixin):
    variety = 2
    context = {
        'title': _('List of created reports - '),
    }


class Create(vxmx.CreateReportMixin):
    form_class = f.CreateSumOfIncomeSumOfExpenseForm
    variety = 2


class Read(vxmx.ReadReportMixin):
    variety = 2
    values = ('sum_of_values',)
