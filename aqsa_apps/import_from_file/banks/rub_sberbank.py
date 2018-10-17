# Author of Aqsa: Yulay Musin
# Sberbank is the main bank of the Russian Federation
from django import forms
from django.utils.translation import ugettext_lazy as _
from aqsa_apps.wallet_tag_etc import currencies
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from aqsa_apps.import_from_file import models as m
import csv
from django.shortcuts import render, redirect

from django.views.decorators.http import require_POST
from aqsa_apps.transaction import models as ta_m
from django.db.transaction import atomic as db_transaction_atomic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy


class RubSberbankForm(forms.Form):
    # date
    date = forms.DateField(label=_('Date'), input_formats=('%d.%m.%Y',))
    # done
    bank_date = forms.DateField(label=_('Bank Date'), input_formats=('%d.%m.%Y',))
    # opid
    bank_ta_id = forms.CharField(label=_('Transaction ID'), max_length=20, required=False)
    # summ
    value_in_curr = forms.DecimalField(label=_('Value in currency'), max_digits=14, decimal_places=2)
    # curr
    currency = forms.ComboField(label=_('Currency'), fields=[forms.ChoiceField(
        choices=currencies.ISO_4217_CURRENCIES + ((643, 'RUR'),)), forms.IntegerField()], required=False)
    # total
    value = forms.DecimalField(label=_('Value in RUB currency'), max_digits=14, decimal_places=2)
    # text
    description = forms.CharField(label=_('Description'), max_length=200, required=False)

    def clean(self):
        cd = self.cleaned_data
        if cd.get('value_in_curr') == 0 and cd.get('value') != 0:
            cd['value_in_curr'] = cd.get('value')
        return cd


def csv_row_for_rub_sberbank_form(row_of_csv, statement_wallet_currency):
    return {
        'date': row_of_csv[0],
        'bank_date': row_of_csv[1],
        'bank_ta_id': row_of_csv[2],
        'value_in_curr': row_of_csv[3].replace(',', '.'),
        # In the Sberbank statement Russian ruble currency indicated not as 'RUB', it's indicated 'RUR'.
        'currency': currencies.currency_title_to_code(row_of_csv[4], plus_curr=((643, 'RUR'),))
        if row_of_csv[4].replace(' ', '') else statement_wallet_currency,
        'value': row_of_csv[5].replace(',', '.'),
        'description': row_of_csv[6],
    }


def value_in_curr_multiply_to_minus_1(value_in_curr, value):
    return value_in_curr * -1 if value < 0 < value_in_curr else value_in_curr


@login_required
def rub_sberbank_check(request, pk):
    statement = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=1, bank='rub_sberbank')

    no_error = True
    errors = []
    num_of_row = 1
    statement_rows = []

    with open(statement.file.path, 'r') as file_csv:
        csv_data = csv.reader(file_csv, delimiter=';')
        csv_data = iter(csv_data)
        # First row of the CSV is titles of cols.
        next(csv_data)
        for csv_row in csv_data:
            try:
                row_data_dict = csv_row_for_rub_sberbank_form(csv_row, statement.wallet.currency)
            except IndexError:
                no_error = False
                errors = (0, {'': _('File does not contain required columns.')})
                statement_rows = []
                break

            form = RubSberbankForm(row_data_dict)

            if form.is_valid():
                cd = form.cleaned_data
                statement_row = (
                    (True, cd.get('date')),
                    (True, cd.get('bank_date')),
                    (True, cd.get('bank_ta_id')),
                    (True, value_in_curr_multiply_to_minus_1(cd.get('value_in_curr'), cd.get('value'))),
                    (True, currencies.get_currency_title(cd.get('currency'))),
                    (True, cd.get('value')),
                    (True, cd.get('description')),
                )

            else:
                no_error = False

                statement_row = []
                for field in form:
                    if field.errors:
                        field = (False, row_data_dict[field.name])
                    else:
                        field = (True, form.cleaned_data.get(field.name))
                    statement_row.append(field)

                errors_of_row = (num_of_row, form.errors)
                errors.append(errors_of_row)

            statement_rows.append(statement_row)
            num_of_row += 1

    if not statement.checked or statement.no_error is None:
        statement.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('Sberbank statement'),
        'import_from_file': statement,
        'titles_of_cols': (f.label for f in RubSberbankForm()),
        'statement_data': statement_rows,
        'errors': errors,
        'notes': (_('After file will be completely imported, you have to correct balance of your wallet manually'),
                  _('As you can see, Sberbank statement have the IDs of transactions ("Transaction ID" column). At the '
                    'next, when you will upload a new file, Aqsa will not add transactions with ID, which already '
                    'exists in any transaction of selected wallet. IDs of transactions is the same in every report, '
                    'which you can get from Sberbank. But some transactions have an ID, which equal to 0 and that ID is'
                    ' not unique. Aqsa will check: do you have a transaction with the same value and with the same bank'
                    ' date and with the ID equal to 0. If answer is NO, then that transaction will be added. Just do '
                    'not edit "Transaction Date in Bank" and "Transaction ID in Bank" and transactions will be not '
                    'duplicated even if you will upload the same Sberbank statement two or more times.'),
                  ),
        'submit_btn': _('Confirm to import data'),
        'links': (m.ImportFromFile.links['list'],),
    })


@require_POST
@login_required
def rub_sberbank_db_records(request, pk):
    statement = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=1, bank='rub_sberbank')

    if not statement.checked or not statement.no_error:
        return redirect(statement.get_check_url())

    existing_bank_ta_id = ta_m.Transaction.objects.filter(owner=request.user, wallet=statement.wallet)\
        .values_list('bank_ta_id', flat=True)

    with open(statement.file.path, 'r') as file_csv:
        csv_data = csv.reader(file_csv, delimiter=';')
        csv_data = iter(csv_data)
        # Needs to skip first iter because first row of the CSV is titles of cols.
        next(csv_data)

        counter = 0
        new_transactions = []
        for csv_row in csv_data:
            counter += 1
            if counter <= statement.num_imported_rows:
                continue
            # FOR DEBUG:
            # if counter >= 2:
            #     continue

            row_data_dict = csv_row_for_rub_sberbank_form(csv_row, statement.wallet.currency)
            form = RubSberbankForm(row_data_dict)
            # We will not check form valid or not because we believe form is valid because we checked CSV file before,
            # but anyway we should to call "is_valid()" for got the "cleaned_data"
            form.is_valid()
            cd = form.cleaned_data

            if cd.get('bank_ta_id') == '0':
                ta_with_0_bank_ta_id = ta_m.Transaction.objects.filter(
                    owner=request.user, wallet=statement.wallet, value=cd.get('value'), bank_ta_id='0',
                    bank_date=cd.get('bank_date')).values_list('id', flat=True)
                if ta_with_0_bank_ta_id:
                    continue
            elif cd.get('bank_ta_id') in existing_bank_ta_id:
                continue

            new_transactions.append(ta_m.Transaction(
                owner=request.user,
                wallet=statement.wallet,

                date=cd.get('date'),
                bank_date=cd.get('bank_date'),
                bank_ta_id=cd.get('bank_ta_id'),
                value_in_curr=value_in_curr_multiply_to_minus_1(cd.get('value_in_curr'), cd.get('value')),
                currency=cd.get('currency'),
                value=cd.get('value'),
                description=cd.get('description'),
            ))

            statement.num_imported_rows += 1
            if not counter % ta_m.Transaction.MAX_NUM_OF_RECORDS_PER_BULK:
                with db_transaction_atomic():
                    statement.save(update_fields=('num_imported_rows',))
                    ta_m.Transaction.objects.bulk_create(new_transactions)
                new_transactions = []
        else:
            if new_transactions:
                with db_transaction_atomic():
                    statement.save(update_fields=('num_imported_rows',))
                    ta_m.Transaction.objects.bulk_create(new_transactions)

    statement.mark_as_finished()

    msg = _('Success. All transactions from your file was added. Your file completely imported.')
    messages.success(request, msg)

    return redirect(reverse_lazy('import_from_file:list'))
