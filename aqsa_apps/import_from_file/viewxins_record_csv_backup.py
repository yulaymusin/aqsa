# Author of Aqsa: Yulay Musin
from aqsa_apps.wallet_tag_etc import models as wte_m
import csv
from . import viewxins_check_csv_backup as vxccb
from . import forms as f
from aqsa_apps.transaction import models as ta_m
from django.db.transaction import atomic as db_transaction_atomic


# <Wallet_Tag_etc
def cleaned_data_for_wallet_model(fcd):
    return {
        'name': fcd['name'],
        'currency': fcd['currency'],
        'description': fcd['description'],
    }


def cleaned_data_for_category_or_for_tag_model(fcd):
    return {
        'name': fcd['name'],
    }


def cleaned_data_for_contact_model(fcd):
    return {
        'name': fcd['name'],
        'description': fcd['description'],
    }


cleaned_data_for_model_of_wallet_tag_etc = {
    wte_m.Wallet: cleaned_data_for_wallet_model,
    wte_m.Category: cleaned_data_for_category_or_for_tag_model,
    wte_m.Tag: cleaned_data_for_category_or_for_tag_model,
    wte_m.Contact: cleaned_data_for_contact_model,
}


def db_recorder_of_csv_of_wallet_tag_etc(path_to_csv, request_user, form_of_wallet_tag_etc, model_of_wallet_tag_etc):
    names_of_wallet_tag_etc_in_csv = []

    existing_objects = model_of_wallet_tag_etc.objects.filter(owner=request_user).values_list('name', flat=True)
    new_objects = []
    with open(path_to_csv, 'r', encoding='utf-8') as file_csv:
        csv_data = csv.reader(file_csv)
        csv_data = iter(csv_data)
        next(csv_data)

        counter = 0
        for csv_row in csv_data:
            form = form_of_wallet_tag_etc(vxccb.csv_row_for_form[form_of_wallet_tag_etc](csv_row))
            # We will not check form valid or not because we believe form is valid because we checked CSV file before,
            # but anyway we should to call "is_valid()" for got the "cleaned_data"
            form.is_valid()
            fcd = form.cleaned_data
            names_of_wallet_tag_etc_in_csv.append(fcd['name'])
            if fcd['name'] not in existing_objects:
                counter += 1
                new_objects.append(model_of_wallet_tag_etc(
                    owner=request_user,
                    **cleaned_data_for_model_of_wallet_tag_etc[model_of_wallet_tag_etc](fcd),
                ))

                if not counter % model_of_wallet_tag_etc.MAX_NUM_OF_RECORDS_PER_BULK:
                    model_of_wallet_tag_etc.objects.bulk_create(new_objects)
                    new_objects = []
        else:
            if new_objects:
                model_of_wallet_tag_etc.objects.bulk_create(new_objects)

    return names_of_wallet_tag_etc_in_csv
# </Wallet_Tag_etc


# <Transaction
def tags_for_transaction(dict_with_tags, str_with_tags):
    tags = []
    if str_with_tags:
        if ';' in str_with_tags:
            for tag in str_with_tags.split(';'):
                tags.append(dict_with_tags[tag])
        else:
            tags.append(dict_with_tags[str_with_tags])
    return tags


def db_recorder_of_transaction(
        path_to_csv, import_from_file, request_user,
        dict_with_wallets, dict_with_categories, dict_with_tags, dict_with_contacts
):
    with open(path_to_csv, 'r', encoding='utf-8') as file_csv:
        csv_data = csv.reader(file_csv)
        csv_data = iter(csv_data)
        next(csv_data)

        pair_of_transfer_dict = {}
        counter = 0
        for csv_row in csv_data:
            counter += 1
            if counter <= import_from_file.num_imported_rows:
                continue

            row_data_dict = vxccb.csv_row_for_transaction_form(csv_row)
            # row_data_dict['wallet_curr'] = dict_with_wallets[csv_row[5]].currency
            # Here could be used "CreateEditIncomeExpenseForm" from transaction.forms, but it makes too many DB queries.
            form = f.Transaction(row_data_dict)
            form.is_valid()
            fcd = form.cleaned_data

            if not fcd.get('transfer'):
                ta = ta_m.Transaction(
                    owner=request_user,
                    date=fcd.get('date'),
                    value=fcd.get('value'),
                    wallet=dict_with_wallets[fcd.get('wallet').name],
                    category=dict_with_categories[fcd.get('category')] if fcd.get('category') else None,
                    description=fcd.get('description'),
                    # tag below
                    currency=fcd.get('currency'),
                    value_in_curr=fcd.get('value_in_curr'),
                    contact=dict_with_contacts[fcd.get('contact')] if fcd.get('contact') else None,
                    not_ignore=fcd.get('not_ignore'),
                    bank_date=fcd.get('bank_date'),
                    bank_ta_id=fcd.get('bank_ta_id'),
                )

                tags_for_ta = tags_for_transaction(dict_with_tags, fcd.get('tag'))

                import_from_file.num_imported_rows += 1
                with db_transaction_atomic():
                    ta.save()
                    ta.tag.add(*tags_for_ta)
                    import_from_file.save(update_fields=('num_imported_rows',))

            elif fcd.get('transfer') and fcd.get('value') > 0:
                row_data_dict = vxccb.csv_row_of_positive_ta_for_ta_pair_transfer_form(row_data_dict)
                pair_of_transfer_dict.update(row_data_dict)

            elif fcd.get('transfer') and fcd.get('value') < 0:
                row_data_dict = vxccb.csv_row_of_negative_ta_for_ta_pair_transfer_form(row_data_dict)
                pair_of_transfer_dict.update(row_data_dict)

                form = f.TransactionPairTransfer(pair_of_transfer_dict)
                form.is_valid()
                fcd = form.cleaned_data
                ta1 = ta_m.Transaction(
                    owner=request_user,
                    transfer=True,
                    date=fcd.get('date'),
                    value=fcd.get('value1'),
                    wallet=dict_with_wallets[fcd.get('wallet1').name],
                    category=dict_with_categories[fcd.get('category')] if fcd.get('category') else None,
                    description=fcd.get('description1'),
                    # tag below
                    currency=fcd.get('currency'),
                    value_in_curr=fcd.get('value_in_curr'),
                    contact=dict_with_contacts[fcd.get('contact')] if fcd.get('contact') else None,
                    bank_date=fcd.get('bank_date1'),
                    bank_ta_id=fcd.get('bank_ta_id1'),
                )
                ta2 = ta_m.Transaction(
                    owner=request_user,
                    transfer=True,
                    date=ta1.date,
                    value=fcd.get('value2'),
                    wallet=dict_with_wallets[fcd.get('wallet2').name],
                    category=ta1.category,
                    description=fcd.get('description2'),
                    # tag below
                    currency=ta1.currency,
                    value_in_curr=ta1.value_in_curr * -1,
                    contact=ta1.contact,
                    bank_date=fcd.get('bank_date2'),
                    bank_ta_id=fcd.get('bank_ta_id2'),
                )

                tags_for_ta1 = tags_for_transaction(dict_with_tags, fcd.get('tag1'))
                tags_for_ta2 = tags_for_transaction(dict_with_tags, fcd.get('tag2'))

                import_from_file.num_imported_rows += 2
                with db_transaction_atomic():
                    ta1.save()
                    ta2.transfer_related = ta1
                    ta2.save()

                    ta1.tag.add(*tags_for_ta1)
                    ta2.tag.add(*tags_for_ta2)
                    import_from_file.save(update_fields=('num_imported_rows',))
# </Transaction
