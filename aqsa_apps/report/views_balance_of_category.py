# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from django.utils.translation import gettext as _
from . import forms as f


class List(vxmx.ListReportMixin):
    variety = 1
    model_labels_and_fields = ('date',
                               'start_date', 'finish_date', 'wallet', 'currency', 'contact', 'exclude_ignored')
    context = {
        'title': _('List of created reports - '),
    }


class Create(vxmx.CreateReportMixin):
    form_class = f.CreateBalanceOfCategoryForm
    variety = 1


class Read(vxmx.ReadReportMixin):
    variety = 1
    values = ('sum_of_values_in_curr', 'category__name', 'category_null')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_data = self.object.data.all().values(*self.values)

        total = sum([x['sum_of_values_in_curr'] if x['sum_of_values_in_curr'] is not None else 0 for x in report_data])

        context.update({
            'total': total,
        })
        return context
