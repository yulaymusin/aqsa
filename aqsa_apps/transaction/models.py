# Author of Aqsa: Yulay Musin
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.wallet_tag_etc import currencies
from django.urls import reverse_lazy


class Transaction(models.Model):
    class Meta:
        db_table = 'transaction'
        ordering = ('-date', '-pk')
        # MAY TO DO: unique_together = (('owner', 'wallet', 'bank_ta_id'),)

    # How many records will be added to DB per one "Transaction.objects.bulk_create()". Using in "import_from_file"
    MAX_NUM_OF_RECORDS_PER_BULK = 50

    owner = models.ForeignKey(User, models.CASCADE)

    # Is money transfer.
    transfer = models.BooleanField(db_index=True, default=False, verbose_name=_('Transfer or Income or Expense'))
    # transfer_related not for show to user, transfer_related needs for update/delete transfer pair.
    transfer_related = models.OneToOneField('self', on_delete=models.CASCADE, null=True)

    date = models.DateField(db_index=True, default=timezone.now, verbose_name=_('Date'))

    # Value in the currency of the wallet, max value is 999,999,999,999.99.
    value = models.DecimalField(db_index=True, max_digits=14, decimal_places=2, verbose_name=_('Value'))

    wallet = models.ForeignKey(wte_m.Wallet, models.PROTECT, verbose_name=_('Wallet'))

    category = models.ForeignKey(wte_m.Category, models.PROTECT, null=True, blank=True, verbose_name=_('Category'))

    description = models.CharField(blank=True, max_length=200, default='', verbose_name=_('Description'))

    tag = models.ManyToManyField(wte_m.Tag, blank=True, verbose_name=_('Tag'))

    # For example: A card (the Wallet) in KRW, but transactions also can be in TRY if user travel in Turkey.
    currency = models.PositiveSmallIntegerField(
        db_index=True, choices=currencies.ISO_4217_CURRENCIES, blank=True, verbose_name=_('Currency'))

    # If transaction not in currency of wallet, then needs a value in that currency.
    value_in_curr = models.DecimalField(
        db_index=True, max_digits=14, decimal_places=2, blank=True, verbose_name=_('Value in Currency'))

    # Borrower or creditor (not allowed in transfer transactions in forms and in views).
    contact = models.ForeignKey(wte_m.Contact, models.PROTECT, null=True, blank=True, verbose_name=_('Contact'))

    # If False, this transaction will be ignored in statistics of dashboard and in reports
    # ("False" not allowed in transfer transactions in forms and in views).
    not_ignore = models.BooleanField(
        db_index=True, default=True, verbose_name=_('Do not ignore in statistics and reports'))

    # <NOT IMPORTANT FIELDS
    # For example: from card in UZS we spend money in Kazakhstan and our issuing bank
    # of the UZS card will convert money to KZT later after fact date.
    bank_date = models.DateField(null=True, blank=True, verbose_name=_('Transaction Date in Bank'))

    # For example: Issuing bank gave a bank statement and every transaction have an ID which would eliminate duplication
    # of transaction...
    bank_ta_id = models.CharField(max_length=20, blank=True, default='', verbose_name=_('Transaction ID in Bank'))
    # </NOT IMPORTANT FIELDS

    def __str__(self):
        return str(self.date) + ' ' + str(self.value) + ' ' + str(self.category) + ' ' + str(self.transfer)

    def get_update_url(self):
        if self.transfer:
            return reverse_lazy('transaction:edit_pair_transfer', kwargs={'pk': self.pk})
        return reverse_lazy('transaction:edit_income_expense', kwargs={'pk': self.pk})

    def get_update_ajax_url(self):
        return reverse_lazy('transaction:ajax_edit', kwargs={'pk': self.pk})

    def get_make_copy_url(self):
        if self.transfer:
            return None
        return reverse_lazy('transaction:copy_transaction', kwargs={'pk': self.pk})

    def get_delete_url(self):
        if self.transfer:
            return reverse_lazy('transaction:delete_pair_transfer', kwargs={'pk': self.pk})
        return reverse_lazy('transaction:delete', kwargs={'pk': self.pk})

    def get_currency_title(self):
        return currencies.get_currency_title(self.currency)

    links = {
        'list': (reverse_lazy('transaction:list'), _('List of transactions'), 'fas fa-list-ul'),
        'list_filter': (reverse_lazy('transaction:list_filter'), _('Search using filter'), 'fas fa-filter'),
        'list_the_edit_mode': (reverse_lazy('transaction:list_the_edit_mode'), _('Edit Mode'), 'fas fa-edit'),
        'new_income_expense': (reverse_lazy('transaction:new_income_expense'), _('New Income or Expense'),
                               'fas fa-shopping-cart'),
        'new_pair_transfer': (reverse_lazy('transaction:new_pair_transfer'), _('New Transfer'), 'fas fa-exchange-alt'),
        'new_income_expense_set': (reverse_lazy('transaction:new_income_expense_set'), _('New Set (Income or Expense)'),
                                   'fas fa-clone'),
    }
