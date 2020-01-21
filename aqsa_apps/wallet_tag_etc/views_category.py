# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from django.db.transaction import atomic as db_transaction_atomic
from aqsa_apps.transaction import models as ta_m
from django.contrib import messages
from django.http import HttpResponseRedirect


class List(vxmx.List):
    model = m.Category
    model_labels_and_fields = ('name',)
    context = {
        'title': _('Categories'),
        'msg_empty_object_list': _('You do not have any category. Click to "New Category" button for create it!'),
    }


class Create(vxmx.Create):
    model = m.Category
    fields = ['name']

    success_url = reverse_lazy('wallet_tag_etc:category_list')
    success_url2 = reverse_lazy('wallet_tag_etc:category_new')

    success_message = _('Category have been created.')
    same_name_error_msg = _('You already have a category with the same name. '
                            'Do not get confused in the future, type another name')
    context = {
        'title': _('New Category'),
    }


class Update(vxmx.Update):
    model = m.Category
    fields = ['name']
    success_message = _('The category was updated.')
    context = {
        'title': _('Edit Category'),
    }


class Delete(vxmx.Delete):
    model = m.Category
    success_message = _('The category was deleted.')
    protected_error_msg = _('Could not delete this category because one or more of your transactions linked to this '
                            'category. Use filter in the list of transactions for find it!')
    context = {
        'title': _('Delete Category'),
        'description': _('Are you sure you want to delete the category shown below?'),
        'labels': [m.Category._meta.get_field(label).verbose_name for label in List.model_labels_and_fields],
        'fields': List.model_labels_and_fields,

        'delete_anyway': _('Unlink all transactions from this category and delete this category.'),
    }

    def except_protected_error(self):
        if self.request.POST.get('delete_anyway'):
            self.object = self.get_object()
            success_url = self.get_success_url()

            with db_transaction_atomic():
                ta_m.Transaction.objects.filter(owner=self.request.user, category=self.object).update(category=None)
                self.object.delete()

            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(success_url)
        messages.info(self.request, _('Use checkbox below for delete this category and unlink all transactions from '
                                      'this category.'))
        return super().except_protected_error()
