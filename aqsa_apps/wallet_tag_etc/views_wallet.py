# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django.db.transaction import atomic as db_transaction_atomic
from aqsa_apps import sql_custom as sql
from aqsa_apps.transaction import models as ta_m
from django.contrib import messages
from django.http import HttpResponseRedirect


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

        'delete_anyway': _('Convert all pairs of transfer transactions, which linked to this wallet, to income-expense '
                           'transactions, then delete all transactions, which linked to this wallet, and finally '
                           'delete this wallet.'),
    }

    def except_protected_error(self):
        if self.request.POST.get('delete_anyway'):
            self.object = self.get_object()
            success_url = self.get_success_url()

            # This query will "convert" transfer transactions to non-transfer (income-expense). Transactions, linked to
            # this wallet, will be not "converted" because anyway they will be deleted after this query. Transfer
            # transactions, only linked to another wallets, will be "converted".
            query = 'UPDATE "transaction" SET "transfer" = false, "transfer_related_id" = NULL where "id" IN' \
                    ' (SELECT "id" FROM "transaction" WHERE "transfer_related_id" IN (SELECT "id" FROM "transaction"' \
                    ' WHERE "wallet_id" = ' + str(self.object.id) + ' AND "transfer" = true AND "owner_id" = ' + \
                    str(self.request.user.id) + ' AND "value" > 0) UNION ALL SELECT "transfer_related_id" as "id"' \
                    ' FROM "transaction" WHERE "wallet_id" = ' + str(self.object.id) + ' AND "transfer" = true AND' \
                    ' "owner_id" = ' + str(self.request.user.id) + ' AND "value" < 0) RETURNING "transfer";'
            with db_transaction_atomic():
                sql.sql(query)
                ta_m.Transaction.objects.filter(owner=self.request.user, wallet=self.object).delete()
                self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(success_url)
        messages.info(self.request, _('Use checkbox below for delete this wallet and all transactions, linked to'
                                      ' this wallet.'))
        return super().except_protected_error()
