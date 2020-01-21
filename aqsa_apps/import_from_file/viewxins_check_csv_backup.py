# Author of Aqsa: Yulay Musin
from aqsa_apps.wallet_tag_etc import currencies
from . import forms as f
import csv


# <Wallet_Tag_etc
def csv_row_for_wallet_form(row_of_csv):
    return {
        'name': row_of_csv[0],
        'currency': currencies.currency_title_to_code(row_of_csv[1]),
        'description': row_of_csv[2],
    }


def csv_row_for_category_or_for_tag_form(row_of_csv):
    return {
        'name': row_of_csv[0],
    }


def csv_row_for_contact_form(row_of_csv):
    return {
        'name': row_of_csv[0],
        'description': row_of_csv[1],
    }


csv_row_for_form = {
    f.Wallet: csv_row_for_wallet_form,
    f.Category: csv_row_for_category_or_for_tag_form,
    f.Tag: csv_row_for_category_or_for_tag_form,
    f.Contact: csv_row_for_contact_form,
}


def csv_checker_of_wallet_tag_etc(path_to_csv, form_of_wallet_tag_etc):
    add_name_and_currency_of_wallet = {
        f.Wallet: lambda name, currency, names_and_curr: names_and_curr.update({name: currency}),
        f.Category: lambda *args: None,
        f.Tag: lambda *args: None,
        f.Contact: lambda *args: None,
    }

    no_error = True

    names_of_wallet_tag_etc_in_csv = []
    names_and_currencies_of_wallets = {}
    with open(path_to_csv, 'r', encoding='utf-8') as file_csv:
        csv_data = csv.reader(file_csv)
        csv_data = iter(csv_data)
        # First row of the CSV is titles of cols.
        next(csv_data)

        for csv_row in csv_data:
            try:
                form = form_of_wallet_tag_etc(csv_row_for_form[form_of_wallet_tag_etc](csv_row))
            except IndexError:
                no_error = False
                break

            # If form is not valid OR name of "wallet_tag_etc" duplicated in the CSV.
            if not form.is_valid() or form.cleaned_data.get('name') in names_of_wallet_tag_etc_in_csv:
                no_error = False
                break

            fcd = form.cleaned_data
            names_of_wallet_tag_etc_in_csv.append(fcd.get('name'))
            # Instead of below... (not recommended use "if ..." inside "for ..." because it's slow)
            # if form_of_wallet_tag_etc == f.Wallet:
            #     names_and_currencies_of_wallets.update({fcd.get('name'): fcd.get('currency')})
            add_name_and_currency_of_wallet[form_of_wallet_tag_etc](
                fcd.get('name'), fcd.get('currency'), names_and_currencies_of_wallets)

    return no_error, names_of_wallet_tag_etc_in_csv, names_and_currencies_of_wallets
# </Wallet_Tag_etc


# <Transaction
def csv_row_for_transaction_form(row_of_csv):
    return {
        'for_check_csv': None,

        'id': row_of_csv[0],
        'transfer': row_of_csv[1],
        'transfer_related': row_of_csv[2],
        'date': row_of_csv[3],
        'value': row_of_csv[4],
        'wallet': row_of_csv[5],
        # 'wallet_curr': names_and_currencies_of_wallets[row_of_csv[5]],
        'wallet_curr': None,
        'category': row_of_csv[6],
        'description': row_of_csv[7],
        'tag': row_of_csv[8],
        'currency': currencies.currency_title_to_code(row_of_csv[9]),
        'value_in_curr': row_of_csv[10],
        'contact': row_of_csv[11],
        'not_ignore': row_of_csv[12],
        'bank_date': row_of_csv[13],
        'bank_ta_id': row_of_csv[14],
    }


def csv_row_of_positive_ta_for_ta_pair_transfer_form(row_data_dict):
    return {
        'for_check_csv': None,

        'date': row_data_dict['date'],
        'value1': row_data_dict['value'],
        'wallet1': row_data_dict['wallet'],
        'wallet1_curr': row_data_dict['wallet_curr'],
        'currency': row_data_dict['currency'],
        'value_in_curr': row_data_dict['value_in_curr'],
        'category': row_data_dict['category'],
        'description1': row_data_dict['description'],
        'tag1': row_data_dict['tag'],
        'contact': row_data_dict['contact'],
        'bank_date1': row_data_dict['bank_date'],
        'bank_ta_id1': row_data_dict['bank_ta_id'],
    }


def csv_row_of_negative_ta_for_ta_pair_transfer_form(row_data_dict):
    return {
        'date2': row_data_dict['date'],
        'value2': row_data_dict['value'],
        'wallet2': row_data_dict['wallet'],
        'wallet2_curr': row_data_dict['wallet_curr'],
        'currency2': row_data_dict['currency'],
        'value_in_curr2': row_data_dict['value_in_curr'],
        'category2': row_data_dict['category'],
        'description2': row_data_dict['description'],
        'tag2': row_data_dict['tag'],
        'contact2': row_data_dict['contact'],
        'bank_date2': row_data_dict['bank_date'],
        'bank_ta_id2': row_data_dict['bank_ta_id'],
    }


def csv_checker_of_transaction(
        path_to_csv,
        names_and_currencies_of_wallets, names_of_categories, names_of_tags, names_of_contacts
):
    no_error = True

    id_of_transactions_in_csv = []
    id_of_transfer_related_ta = []
    # Key will be ID of transaction with positive value.
    transfer_transactions = {}
    id_of_positive_ta_in_transfer_pair_right_now = None
    with open(path_to_csv, 'r', encoding='utf-8') as file_csv:
        csv_data = csv.reader(file_csv)
        csv_data = iter(csv_data)
        # First row of the CSV is titles of cols.
        next(csv_data)
        for csv_row in csv_data:
            try:
                row_data_dict = csv_row_for_transaction_form(csv_row)
                row_data_dict['for_check_csv'] = True
                row_data_dict['wallet_curr'] = names_and_currencies_of_wallets[csv_row[5]]
            except IndexError:
                row_data_dict = csv_row_for_transaction_form(csv_row)
                row_data_dict['for_check_csv'] = True
                row_data_dict['wallet_curr'] = names_and_currencies_of_wallets[csv_row[5]]
                no_error = False
                break

            form = f.Transaction(row_data_dict)
            if not form.is_valid():
                no_error = False
                break

            fcd = form.cleaned_data

            # Pair of transfer should be always together. Right after the positive ta should be the negative ta.
            if not fcd.get('transfer') and id_of_positive_ta_in_transfer_pair_right_now is not None:
                no_error = False
                break

            # If id duplicated.
            if fcd.get('id'):
                if fcd.get('id') in id_of_transactions_in_csv:
                    no_error = False
                    break
                id_of_transactions_in_csv.append(fcd.get('id'))

            # If transfer_related duplicated.
            if fcd.get('transfer_related'):
                if fcd.get('transfer_related') in id_of_transfer_related_ta:
                    no_error = False
                    break
                id_of_transfer_related_ta.append(fcd.get('transfer_related'))

            # <If wallet_tag_etc of transaction does not exists.
            if fcd.get('wallet').name not in names_and_currencies_of_wallets:
                no_error = False
                break
            if fcd.get('category') and fcd.get('category') not in names_of_categories:
                no_error = False
                break
            if fcd.get('tag'):
                if ';' in fcd.get('tag'):
                    for tag in fcd.get('tag').split(';'):
                        if tag not in names_of_tags:
                            no_error = False
                            break
                else:
                    if fcd.get('tag') not in names_of_tags:
                        no_error = False
                        break
            if fcd.get('contact') and fcd.get('contact') not in names_of_contacts:
                no_error = False
                break
            # </If wallet_tag_etc of transaction does not exists.

            if fcd.get('transfer') and fcd.get('value') > 0:
                # Now we will work with pair of transfer ta (transactions), pair with ID of positive value ta
                id_of_positive_ta_in_transfer_pair_right_now = fcd.get('id')
                # Transaction with positive value should be first in the CSV
                row_data_dict = csv_row_of_positive_ta_for_ta_pair_transfer_form(row_data_dict)
                row_data_dict['for_check_csv'] = True
                transfer_transactions.update({fcd.get('id'): row_data_dict})

            elif fcd.get('transfer') and fcd.get('value') < 0:
                # If ta with negative does not linked to the ta with positive value
                # (if this row not ta of the pair with which we work right now).
                if id_of_positive_ta_in_transfer_pair_right_now != fcd.get('transfer_related'):
                    no_error = False
                    break
                try:
                    row_data_dict = csv_row_of_negative_ta_for_ta_pair_transfer_form(row_data_dict)
                    transfer_transactions[fcd.get('transfer_related')].update(row_data_dict)
                except KeyError:
                    no_error = False
                    break
                id_of_positive_ta_in_transfer_pair_right_now = None

    for id_of_positive, transfer_pair in transfer_transactions.items():
        form = f.TransactionPairTransfer(transfer_pair)
        if not form.is_valid():
            no_error = False
            break

    return no_error
# </Transaction
