# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django.db.transaction import atomic as db_transaction_atomic
from aqsa_apps.transaction import models as ta_m
from django.contrib import messages
from django.http import HttpResponseRedirect


class List(vxmx.List):
    model = m.Contact
    model_labels_and_fields = ('name', 'description',)
    context = {
        'title': _('My Contacts'),
        'msg_empty_object_list': _('You do not have any contact. Click to "New Contact" button for create it!'),
    }


class Create(vxmx.Create):
    model = m.Contact
    fields = ['name', 'description']

    success_url = reverse_lazy('wallet_tag_etc:contact_list')
    success_url2 = reverse_lazy('wallet_tag_etc:contact_new')

    success_message = _('Contact have been created.')
    same_name_error_msg = _('You already have a contact with the same name. '
                            'Do not get confused in the future, type another name')
    context = {
        'title': _('New Contact'),
    }


class Update(vxmx.Update):
    model = m.Contact
    fields = ['name', 'description']
    success_message = _('The contact was updated.')
    context = {
        'title': _('Edit Contact'),
    }


class Delete(vxmx.Delete):
    model = m.Contact
    success_message = _('The contact was deleted.')
    protected_error_msg = _('Could not delete this contact because one or more of your transactions linked to this '
                            'contact. Use filter in the list of transactions for find it!')
    context = {
        'title': _('Delete Contact'),
        'description': _('Are you sure you want to delete the contact shown below?'),
        'labels': [m.Contact._meta.get_field(label).verbose_name for label in List.model_labels_and_fields],
        'fields': List.model_labels_and_fields,

        'delete_anyway': _('Unlink all transactions from this contact and delete this contact.'),
    }

    def except_protected_error(self):
        if self.request.POST.get('delete_anyway'):
            self.object = self.get_object()
            success_url = self.get_success_url()

            with db_transaction_atomic():
                ta_m.Transaction.objects.filter(owner=self.request.user, contact=self.object).update(contact=None)
                self.object.delete()

            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(success_url)
        messages.info(self.request, _('Use checkbox below for delete this contact and unlink all transactions from '
                                      'this contact.'))
        return super().except_protected_error()
