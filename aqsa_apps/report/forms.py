# Author of Aqsa: Yulay Musin
from aqsa_apps import mixins as mix
from django import forms
from . import models as m
from aqsa_apps.wallet_tag_etc import currencies
from django.utils.translation import gettext_lazy as _
from aqsa_apps.wallet_tag_etc import models as wte_m


class CreateBalanceOfCategoryForm(mix.FilterFieldsInFormByRequestUser, forms.ModelForm):
    filter_fields = ('wallet', 'contact')

    class Meta:
        model = m.Report
        fields = ('start_date', 'finish_date', 'wallet', 'currency', 'contact', 'exclude_ignored')

    currency = forms.ChoiceField(
        choices=(('', '---------'),) + currencies.ISO_4217_CURRENCIES, label=_('Currency parameter'))


class CreateSumOfIncomeSumOfExpenseForm(mix.FilterFieldsInFormByRequestUser, forms.ModelForm):
    filter_fields = ('wallet', 'contact')

    class Meta:
        model = m.Report
        fields = ('start_date', 'finish_date', 'wallet', 'contact', 'exclude_ignored')

    wallet = forms.ModelMultipleChoiceField(
        queryset=wte_m.Wallet.objects, label=_('Wallet - #1'),
        help_text=_('If you want to choose few wallets, they should be in the same currency.'))

    def clean(self):
        cd = self.cleaned_data
        if cd.get('wallet') and len(cd.get('wallet')) >= 2:
            wallet_currency = cd.get('wallet')[0].currency
            for w in cd.get('wallet'):
                if w.currency != wallet_currency:
                    msg = _('All selected wallets should be in the same currency.')
                    self.add_error('wallet', msg)
        return cd
