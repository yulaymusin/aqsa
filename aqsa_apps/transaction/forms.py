# Author of Aqsa: Yulay Musin
from aqsa_apps import mixins as mix
from django import forms
from . import models as m
from django.utils.translation import gettext_lazy as _
from . import formxins as fx
from django.utils import timezone
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.wallet_tag_etc import currencies


class CreateEditIncomeExpenseForm(mix.FilterFieldsInFormByRequestUser, forms.ModelForm):
    filter_fields = ('wallet', 'category', 'tag', 'contact')

    class Meta:
        model = m.Transaction
        exclude = ('owner', 'transfer', 'transfer_related')
        help_texts = {
            'date': _('Required.'),
            'value': _('Required.'),
            'wallet': _('Required.'),
            'category': _('Optional.'),
            'description': _('Optional.'),
            'tag': _('Optional.'),

            'currency': _('Optional. Leave empty and transaction will be saved with the currency of selected wallet.'),
            'value_in_curr': _('Optional. Leave empty if currency of selected wallet and currency of your transaction '
                               'is the same.'),

            'contact': _('Did you gave money to someone or take from somebody? Choose your contact here.'),

            'not_ignore': _('If you will uncheck, then this transaction will be ignored in statistics of income/expense'
                            ' in dashboard and in the income/expense reports.'),

            'bank_date': _('Optional.'),
            'bank_ta_id': _('Optional.'),
        }

    def clean(self):
        return fx.clean_for_income_expense_form(self.cleaned_data, self.add_error)


class CreateEditPairTransferForm(mix.FilterFieldsInFormByRequestUser, forms.Form):
    filter_fields = ('wallet1', 'wallet2', 'category', 'tag1', 'tag2', 'contact')

    # One field for both transactions
    date = forms.DateField(
        initial=timezone.now(), label=_('Date of money transfer'),
        help_text=_('Required. This date will be saved in both transactions.'))

    value1 = forms.DecimalField(
        max_digits=14, decimal_places=2, label=_('Value - #1'),
        help_text=_('Required. How much money goes to the receiving wallet? Fill a positive value.'))
    value2 = forms.DecimalField(
        required=False, max_digits=14, decimal_places=2, label=_('Value - #2'),
        help_text=_('Required if wallets in different currencies. How much money spend (goes from) the sending wallet? '
                    'Fill a negative value.'))

    wallet1 = forms.ModelChoiceField(
        queryset=wte_m.Wallet.objects, label=_('Wallet - #1'),
        help_text=_('Required. Wallet, which receive the money.'))
    wallet2 = forms.ModelChoiceField(
        queryset=wte_m.Wallet.objects, label=_('Wallet - #2'),
        help_text=_('Required. Wallet, from which the money goes.'))

    # One field for both transactions
    currency = forms.ChoiceField(
        required=False, choices=(('', '---------'),) + currencies.ISO_4217_CURRENCIES, label=_('Currency'),
        help_text=_('Required if wallets in different currencies. '
                    'Selected currency will be saved in both transactions.'))

    # One field for both transactions
    value_in_curr = forms.DecimalField(
        required=False, max_digits=14, decimal_places=2, label=_('Value in currency'),
        help_text=_('Required if wallets in different currencies. '
                    'How much money (in selected currency) do you transfer between wallets? Fill a positive value.'))

    # One field for both transactions
    category = forms.ModelChoiceField(
        required=False, queryset=wte_m.Category.objects, label=_('Category'),
        help_text=_('Optional. Selected category will be saved in both transactions.'))

    description1 = forms.CharField(
        required=False, max_length=200, label=_('Description - #1'),
        help_text=_('Optional. Description of the transaction that replenishes the receiving wallet.'))
    description2 = forms.CharField(
        required=False, max_length=200, label=_('Description - #2'),
        help_text=_('Optional. Description of the transaction that withdraws money from the sending wallet.'))

    tag1 = forms.ModelMultipleChoiceField(
        required=False, queryset=wte_m.Tag.objects, label=_('Tag - #1'),
        help_text=_('Optional. Tags for the transaction that replenishes the receiving wallet.'))
    tag2 = forms.ModelMultipleChoiceField(
        required=False, queryset=wte_m.Tag.objects, label=_('Tag - #2'),
        help_text=_('Optional. Tags for the transaction that withdraws money from the sending wallet.'))

    # One field for both transactions
    contact = forms.ModelChoiceField(
        required=False, queryset=wte_m.Contact.objects, label=_('Contact'),
        help_text=_('Optional. Selected contact will be saved in both transactions.'))

    bank_date1 = forms.DateField(
        required=False, label=_('Transaction Date in Bank - #1'),
        help_text=_('Optional. Date of the transaction in the bank that takes the money.'))
    bank_date2 = forms.DateField(
        required=False, label=_('Transaction Date in Bank - #2'),
        help_text=_('Optional. Date of the transaction in the bank that sends the money.'))

    bank_ta_id1 = forms.CharField(
        required=False, max_length=20, label=_('Transaction ID in Bank - #1'),
        help_text=_('Optional. ID of the transaction in the bank that takes the money.'))
    bank_ta_id2 = forms.CharField(
        required=False, max_length=20, label=_('Transaction ID in Bank - #2'),
        help_text=_('Optional. ID of the transaction in the bank that sends the money.'))

    def clean(self):
        return fx.clean_for_pair_transfer_form(self.cleaned_data, self.add_error)


# EditAloneTransferForm for ".views_ajax.ajax_update"
class EditAloneTransferForm(mix.FilterFieldsInFormByRequestUser, forms.ModelForm):
    filter_fields = ('tag',)

    class Meta:
        model = m.Transaction
        fields = ('description', 'tag', 'bank_date', 'bank_ta_id')
