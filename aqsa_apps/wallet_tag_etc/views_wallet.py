# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy


class List(vxmx.List):
    model = m.Wallet
    model_labels_and_fields = ('name', 'currency', 'description',)
    context = {
        'title': _('My Wallets'),
        'msg_empty_object_list': _('You do not have any wallet. Click to "New Wallet" button for create it!'),
    }


class Create(vxmx.Create):
    model = m.Wallet
    fields = ['name', 'currency', 'description']

    success_url = reverse_lazy('wallet_tag_etc:wallet_list')
    success_url2 = reverse_lazy('wallet_tag_etc:wallet_new')

    success_message = _('Wallet have been created.')
    same_name_error_msg = _('You already have a wallet with the same name. '
                            'Do not get confused in the future, type another name')
    context = {
        'title': _('New Wallet'),
    }


class Update(vxmx.Update):
    model = m.Wallet
    fields = ['name', 'description']
    success_message = _('The wallet was updated.')
    context = {
        'title': _('Edit Wallet'),
    }


class Delete(vxmx.Delete):
    model = m.Wallet
    success_message = _('The wallet was deleted.')
    protected_error_msg = _('Could not delete this wallet because one or more of your transactions linked to this '
                            'wallet. Use filter in the list of transactions for find it!')
    context = {
        'title': _('Delete Wallet'),
        'description': _('Are you sure you want to delete the wallet shown below?'),
        'labels': [m.Wallet._meta.get_field(label).verbose_name for label in List.model_labels_and_fields],
        'fields': List.model_labels_and_fields,
    }
