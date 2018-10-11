# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy


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
    }
