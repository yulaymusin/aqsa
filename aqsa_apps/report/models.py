# Author of Aqsa: Yulay Musin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.wallet_tag_etc import currencies
from django.urls import reverse_lazy


class Report(models.Model):
    class Meta:
        db_table = 'report'
        ordering = ('-pk',)

    varieties = (
        (1, _('Balance of every Category (Sum Of Transactions), also total balance')),
        (2, _('Sum Of Income')),
        (3, _('Sum Of Expense')),
        # TODO next reports
        # (4, _('Sum Of Income By Wallet')),
        # (5, _('Sum Of Expense By Wallet')),
        # (6, _('Sum Of Income By Category')),
        # (7, _('Sum Of Expense By Category')),
        # (8, _('Sum Of Income By Tag')),
        # (9, _('Sum Of Expense By Tag')),
        # (10, _('Sum Of Income By Currency')),
        # (11, _('Sum Of Expense By Currency')),
        # (12, _('Balance (Sum Of Transactions) By Contact')),
    )

    owner = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name=_('Date of create report'))
    variety = models.PositiveSmallIntegerField(choices=varieties, verbose_name=_('Variety of uploaded file'))

    # <FILTERS.
    start_date = models.DateField(null=True, blank=True, verbose_name=_('Start Date parameter'))
    finish_date = models.DateField(null=True, blank=True, verbose_name=_('Finish Date parameter'))
    wallet = models.ManyToManyField(wte_m.Wallet, blank=True, verbose_name=_('Wallet parameter'))
    # category = models.ForeignKey(wte_m.Category, models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    # tag = models.ForeignKey(wte_m.Tag, models.SET_NULL, null=True, blank=True, verbose_name=_('Tag'))
    currency = models.PositiveSmallIntegerField(
        null=True, choices=currencies.ISO_4217_CURRENCIES, blank=True, verbose_name=_('Currency parameter'))
    contact = models.ForeignKey(
        wte_m.Contact, models.SET_NULL, null=True, blank=True, verbose_name=_('Contact parameter'))
    exclude_ignored = models.BooleanField(default=True, verbose_name=_('Exclude Ignored parameter'))
    # </FILTERS.

    def __str__(self):
        return self.get_variety_name() + ', ' + str(self.date)

    def get_variety_name(self):
        for va in self.varieties:
            if va[0] == self.variety:
                return va[1]

    read_urls = {
        1: 'balance_of_category_read',
        2: 'sum_of_income_read',
        3: 'sum_of_expense_read',
    }

    def get_read_url(self):
        return reverse_lazy('report:' + self.read_urls[self.variety], kwargs={'pk': self.pk})

    def get_currency_title(self):
        if self.currency is not None:
            return currencies.get_currency_title(self.currency)

    links = {
        0: {
            'create': (reverse_lazy('report:balance_of_category_create'), _('Create "Balance of Category" report'),
                       'fas fa-calculator'),
            'list': (reverse_lazy('report:balance_of_category_list'), _('"Balance of Category" reports'),
                     'fas fa-list-ul'),
        },
        1: {
            'create': (reverse_lazy('report:sum_of_income_create'), _('Create "Sum of Income" report'),
                       'fas fa-calculator'),
            'list': (reverse_lazy('report:sum_of_income_list'), _('"Sum of Income" reports'),
                     'fas fa-list-ul'),
        },
        2: {
            'create': (reverse_lazy('report:sum_of_expense_create'), _('Create "Sum of Expense" report'),
                       'fas fa-calculator'),
            'list': (reverse_lazy('report:sum_of_expense_list'), _('"Sum of Expense" reports'),
                     'fas fa-list-ul'),
        },
    }


class ReportData(models.Model):
    class Meta:
        db_table = 'report_data'
        ordering = ('-sum_of_values', '-sum_of_values_in_curr')

    report = models.ForeignKey(Report, models.CASCADE, related_name='data')
    # TODO for the next reports
    # Sum of values of currency of wallet.
    sum_of_values = models.DecimalField(
        db_index=True, null=True, max_digits=20, decimal_places=2,
        verbose_name=_('Sum Of "Values" (in currency of wallets) of Transactions'))
    sum_of_values_in_curr = models.DecimalField(
        db_index=True, null=True, max_digits=20, decimal_places=2,
        verbose_name=_('Sum Of "Values in currency" of Transactions'))

    # TODO for the next reports
    # wallet = models.ForeignKey(wte_m.Wallet, models.SET_NULL, null=True, blank=True, verbose_name=_('Wallet'))
    category = models.ForeignKey(wte_m.Category, models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    # This field for sum of transactions without (IS NULL) category.
    category_null = models.BooleanField(default=False)
    # tag = models.ForeignKey(wte_m.Tag, models.SET_NULL, null=True, blank=True, verbose_name=_('Tag'))
    # currency = models.PositiveSmallIntegerField(
    #     null=True, choices=currencies.ISO_4217_CURRENCIES, blank=True, verbose_name=_('Currency'))
    # contact = models.ForeignKey(wte_m.Contact, models.SET_NULL, null=True, blank=True, verbose_name=_('Contact'))
