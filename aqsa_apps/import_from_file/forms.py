# Author of Aqsa: Yulay Musin
from aqsa_apps import mixins as mix
from django import forms
from aqsa_apps.import_from_file import models as m
from django.utils.translation import ugettext_lazy as _

from aqsa_apps.wallet_tag_etc import validators as wte_v
from . import validators as v
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.wallet_tag_etc.currencies import ISO_4217_CURRENCIES
from aqsa_apps.transaction import formxins as ta_fx


class UploadBankStatementForm(mix.FilterFieldsInFormByRequestUser, forms.ModelForm):
    filter_fields = ('wallet',)

    class Meta:
        model = m.ImportFromFile
        fields = ('file', 'wallet', 'bank')
        widgets = {'file': forms.FileInput(attrs={'accept': '.csv, .txt'})}
        help_texts = {
            'file': _('Choose bank statement.'),
            'wallet': _('Select wallet, which is related with an uploading bank statement.'),
            'bank': _('Select bank, which is related with an uploading bank statement.'),
        }

    def clean(self):
        cd = self.cleaned_data

        # If user select, for example, bank for RUB currency, but selected wallet in another currency.
        if ta_fx.is_nnt(cd.get('wallet')) and ta_fx.is_nnt(cd.get('bank')) \
                and cd.get('wallet').get_currency_title()[:3].lower() != cd.get('bank')[:3]:
            msg = _('Currency of selected bank and currency of selected wallet is different.')
            self.add_error('bank', msg)

        return cd


class UploadBackupOrCSVForm(forms.ModelForm):
    variety = forms.CharField(label=m.ImportFromFile._meta.get_field('variety').verbose_name,
                              widget=forms.RadioSelect(choices=m.ImportFromFile.varieties[1:]))

    class Meta:
        model = m.ImportFromFile
        fields = ('file', 'variety')
        widgets = {'file': forms.FileInput(attrs={'accept': '.csv, .zip'})}
        help_texts = {
            'file': _('Choose a Backup File or CSV.'),
            'variety': _('Specify what kind of file do you want to upload.'),
        }


class Wallet(forms.ModelForm):
    class Meta:
        model = wte_m.Wallet
        exclude = ('owner',)


class Category(forms.ModelForm):
    class Meta:
        model = wte_m.Category
        exclude = ('owner',)


class Tag(forms.ModelForm):
    class Meta:
        model = wte_m.Tag
        exclude = ('owner',)


class Contact(forms.ModelForm):
    class Meta:
        model = wte_m.Contact
        exclude = ('owner',)


class Transaction(forms.Form):
    for_check_csv = forms.BooleanField(required=False)

    id = forms.IntegerField(min_value=1, required=False)

    # "transfer" could be Boolean, but will be better, if user can use only "-" and "+" symbols
    transfer = forms.CharField(min_length=1, max_length=1, validators=[v.plus_minus_symbol])
    transfer_related = forms.IntegerField(min_value=1, required=False)

    date = forms.DateField()
    value = forms.DecimalField(max_digits=14, decimal_places=2)
    wallet = forms.CharField(max_length=50, validators=[wte_v.two_or_more_spaces])
    wallet_curr = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])
    category = forms.CharField(max_length=50, required=False)
    description = forms.CharField(max_length=200, required=False)
    tag = forms.CharField(max_length=50, required=False)

    currency = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])
    value_in_curr = forms.DecimalField(max_digits=14, decimal_places=2)

    contact = forms.CharField(max_length=50, required=False)

    # "not_ignore" could be Boolean, but will be better, if user can use only "-" and "+" symbols
    not_ignore = forms.CharField(min_length=1, max_length=1, validators=[v.plus_minus_symbol])

    bank_date = forms.DateField(required=False)
    bank_ta_id = forms.CharField(max_length=20, required=False)

    def clean(self):
        cd = self.cleaned_data

        cd['transfer'] = True if cd.get('transfer') == '+' else False
        cd['wallet'] = wte_m.Wallet(name=cd.get('wallet'), currency=cd.get('wallet_curr'))
        cd['not_ignore'] = True if cd.get('not_ignore') == '+' else False

        if cd.get('for_check_csv'):
            # <If Income/expense (not transfer).
            # Check fields which not for income/expense.
            if not cd.get('transfer') and ta_fx.is_num(cd.get('transfer_related')):
                msg = _('This field should be used only in money transfer transactions')
                self.add_error('transfer_related', msg)

            if not cd.get('transfer'):
                ta_fx.clean_for_income_expense_form(cd, self.add_error, with_auto_fill=False)
            # </If Income/expense (not transfer).

            # <If transfer transaction.
            # If "value" bigger than 0, but not "id".
            if cd.get('transfer') and not cd.get('id') and ta_fx.is_num(cd.get('value')) \
                    and cd.get('value') > 0:
                msg = _('If "Value" is bigger than 0, then "id" should not be empty.')
                self.add_error('id', msg)

            # If "value" bigger than 0, but "transfer_related".
            if cd.get('transfer') and cd.get('transfer_related') and ta_fx.is_num(cd.get('value')) \
                    and cd.get('value') > 0:
                msg = _('If "Value" is bigger than 0, then "transfer_related" should be empty.')
                self.add_error('transfer_related', msg)

            # If "value" less than 0, but not "transfer_related".
            if cd.get('transfer') and not ta_fx.is_num(cd.get('transfer_related')) \
                    and ta_fx.is_num(cd.get('value')) and cd.get('value') < 0:
                msg = _('If "Value" is less than 0, then "transfer_related" should not be empty.')
                self.add_error('transfer_related', msg)

            # not_ignore should be True
            if cd.get('transfer') and cd.get('not_ignore') is not True:
                msg = _('This field should be True in money transfer transactions.')
                self.add_error('not_ignore', msg)
            # </If transfer transaction.

        return cd


class TransactionPairTransfer(forms.Form):
    for_check_csv = forms.BooleanField(required=False)

    date = forms.DateField()
    date2 = forms.DateField()

    value1 = forms.DecimalField(max_digits=14, decimal_places=2)
    value2 = forms.DecimalField(max_digits=14, decimal_places=2)

    wallet1 = forms.CharField(max_length=50, validators=[wte_v.two_or_more_spaces])
    wallet1_curr = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])
    wallet2 = forms.CharField(max_length=50, validators=[wte_v.two_or_more_spaces])
    wallet2_curr = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])

    currency = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])
    currency2 = forms.ComboField(fields=[forms.ChoiceField(choices=ISO_4217_CURRENCIES), forms.IntegerField()])
    value_in_curr = forms.DecimalField(max_digits=14, decimal_places=2)
    value_in_curr2 = forms.DecimalField(max_digits=14, decimal_places=2)

    category = forms.CharField(max_length=50, required=False)
    category2 = forms.CharField(max_length=50, required=False)

    description1 = forms.CharField(max_length=200, required=False)
    description2 = forms.CharField(max_length=200, required=False)

    tag1 = forms.CharField(max_length=50, required=False)
    tag2 = forms.CharField(max_length=50, required=False)

    contact = forms.CharField(max_length=50, required=False)
    contact2 = forms.CharField(max_length=50, required=False)

    bank_date1 = forms.DateField(required=False)
    bank_date2 = forms.DateField(required=False)
    bank_ta_id1 = forms.CharField(max_length=20, required=False)
    bank_ta_id2 = forms.CharField(max_length=20, required=False)

    def clean(self):
        def value1_should_be_equal_to_value2(value, value2, err_in_field, msg):
            if ta_fx.is_nnt(value) and ta_fx.is_nnt(value2) and value != value2:
                self.add_error(err_in_field, msg)

        cd = self.cleaned_data

        cd['wallet1'] = wte_m.Wallet(name=cd.get('wallet1'), currency=cd.get('wallet1_curr'))
        if cd.get('wallet1') != cd.get('wallet2'):
            cd['wallet2'] = wte_m.Wallet(name=cd.get('wallet2'), currency=cd.get('wallet2_curr'))
        else:
            cd['wallet2'] = cd['wallet1']

        if cd.get('for_check_csv'):
            # If date and date2 not the same.
            value1_should_be_equal_to_value2(cd.get('date'), cd.get('date2'), 'date2',
                                             _('Date should be the same in both transactions.'))

            # If currency and currency2 not the same.
            value1_should_be_equal_to_value2(cd.get('currency'), cd.get('currency2'), 'currency2',
                                             _('Currency should be the same in both transactions.'))

            # If value_in_curr + value_in_curr2 not equal to 0.
            if ta_fx.is_nnt(cd.get('value_in_curr')) and ta_fx.is_nnt(cd.get('value_in_curr2')) \
                    and cd.get('value_in_curr') + cd.get('value_in_curr2') != 0:
                msg = _('Sum of "Value_in_curr" both transactions should be equal to 0.')
                self.add_error('value_in_curr2', msg)

            # If category and category2 not the same.
            value1_should_be_equal_to_value2(cd.get('category'), cd.get('category2'), 'category2',
                                             _('Category should be the same in both transactions.'))

            # If contact and contact2 not the same.
            value1_should_be_equal_to_value2(cd.get('contact'), cd.get('contact2'), 'contact2',
                                             _('Contact should be the same in both transactions.'))

            ta_fx.clean_for_pair_transfer_form(cd, self.add_error, with_auto_fill=False)

        return cd
