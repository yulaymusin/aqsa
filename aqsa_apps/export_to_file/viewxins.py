# Author of Aqsa: Yulay Musin
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse
import os
from aqsa_apps.wallet_tag_etc.currencies import get_currency_title
from aqsa_apps.wallet_tag_etc import models as wte_m
import random
from aqsa_apps.transaction import models as ta_m
from django.conf import settings
import csv
from django.core.paginator import Paginator


NUM_OF_RECORDS = 100  # FOR PAGINATOR


def render_or_file_as_http(request, file_path, no_errors, context={}, content_type='text/csv'):
    if not no_errors:
        context = {'title': _('Could not export your data'), 'message': ''} if not context else context
        return render(request=request, template_name='export_to_file/error.html', context=context)

    # <THE FILE AS HttpResponse.
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        # Browser will show the dialog.
        response['Content-Description'] = 'File Transfer'
        response['Content-Disposition'] = 'attachment;'
    # </THE FILE AS HttpResponse.

    # Let's save space in our server.
    os.remove(file_path)
    return response


def export_model_objects_to_csv(request, csv_file_name, model, return_render_or_file_as_http=False):
    # Write a row to the CSV.
    def write_transaction_row():
        csv_writer.writerow([
            t['id'],
            '+' if t['transfer'] else '-',
            t['transfer_related__id'],
            t['date'],
            t['value'],
            t['wallet__name'],
            t['category__name'],
            t['description'],
            t['tag__name'],
            get_currency_title(t['currency']),
            t['value_in_curr'],
            t['contact__name'],
            '+' if t['not_ignore'] else '-',
            t['bank_date'],
            t['bank_ta_id'],
        ])

    msg = _('Sorry, something wrong')
    no_errors = False

    if not csv_file_name and model == wte_m.Wallet:
        csv_file_name = 'user_' + str(request.user.id) + '_wallet_' + str(random.randint(1111, 9999)) + '.csv'
    elif not csv_file_name and model == wte_m.Category:
        csv_file_name = 'user_' + str(request.user.id) + '_category_' + str(random.randint(1111, 9999)) + '.csv'
    elif not csv_file_name and model == wte_m.Tag:
        csv_file_name = 'user_' + str(request.user.id) + '_tag_' + str(random.randint(1111, 9999)) + '.csv'
    elif not csv_file_name and model == wte_m.Contact:
        csv_file_name = 'user_' + str(request.user.id) + '_contact_' + str(random.randint(1111, 9999)) + '.csv'
    elif not csv_file_name and model == ta_m.Transaction:
        csv_file_name = 'user_' + str(request.user.id) + '_transaction_' + str(random.randint(1111, 9999)) + '.csv'
    csv_file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('export_to_file', csv_file_name))

    # <TITLES OF COLUMNS OF CSV FILE
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'export_to_file')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'export_to_file'))
    # Can not write "with open", unless PermissionDenied will be raised.
    f = open(csv_file_path, 'w', encoding='utf-8')
    try:
        csv_writer = csv.writer(f)

        if model == wte_m.Wallet:
            csv_writer.writerow(['name', 'currency', 'description'])
        elif model == wte_m.Category or model == wte_m.Tag:
            csv_writer.writerow(['name'])
        elif model == wte_m.Contact:
            csv_writer.writerow(['name', 'description'])
        elif model == ta_m.Transaction:
            csv_writer.writerow(['id', 'transfer', 'transfer_related__id', 'date', 'value', 'wallet__name',
                                 'category__name', 'description', 'tag__name', 'currency', 'value_in_curr',
                                 'contact__name', 'not_ignore', 'bank_date', 'bank_ta_id'])
        no_errors = True
    finally:
        f.close()
    # </TITLES OF COLUMNS OF CSV FILE

    # <EXPORT TRANSACTIONS TO CSV
    if no_errors:
        if model == wte_m.Wallet:
            values = ('name', 'currency', 'description')
        elif model == wte_m.Category or model == wte_m.Tag:
            values = ('name',)
        elif model == wte_m.Contact:
            values = ('name', 'description')
        elif model == ta_m.Transaction:
            values = ('id', 'transfer', 'transfer_related__id', 'date', 'value', 'wallet__name',
                      'category__name', 'description', 'tag__name', 'currency', 'value_in_curr',
                      'contact__name', 'not_ignore', 'bank_date', 'bank_ta_id')

        objects = model.objects.filter(owner=request.user)\
            .values(*(v for v in values))

        if model == ta_m.Transaction:
            objects = objects.order_by('date', 'pk')

        # We have to paginate query unless if user have a lot of transactions, DB will work slowly and we can spend more
        # resource of RAM
        paginator = Paginator(objects, NUM_OF_RECORDS)

        for i in range(1, paginator.num_pages+1):
            objects = paginator.page(i)

            f = open(csv_file_path, 'a', encoding='utf-8')
            try:
                csv_writer = csv.writer(f)

                if model == wte_m.Wallet:
                    for obj in objects:
                        csv_writer.writerow([obj['name'], get_currency_title(obj['currency']),
                                             obj['description']])
                elif model == wte_m.Category or model == wte_m.Tag:
                    for obj in objects:
                        csv_writer.writerow([obj['name']])
                elif model == wte_m.Contact:
                    for obj in objects:
                        csv_writer.writerow([obj['name'], obj['description']])
                elif model == ta_m.Transaction and len(objects) > 0:
                    # This will be, in loop, wrote to the CSV.
                    t = objects[0]
                    for transaction in objects[1:]:
                        if t['id'] == transaction['id']:
                            t['tag__name'] = t['tag__name'] + ';' + transaction['tag__name']
                        else:
                            write_transaction_row()
                            t = transaction  # after write a transaction to the CSV, put a next transaction to "t"
                    else:
                        write_transaction_row()

            finally:
                f.close()
    # </EXPORT TRANSACTIONS TO CSV

    # <CHECK FILE EXISTS OR NOT, JUST IN CASE
    if no_errors:
        if not os.path.isfile(csv_file_path):
            no_errors = False
            msg = _('Sorry, something very bad')
    # </CHECK FILE EXISTS OR NOT, JUST IN CASE

    if model == wte_m.Wallet:
        title = _('Could not export your wallets to CSV file')
    elif model == wte_m.Category:
        title = _('Could not export your categories to CSV file')
    elif model == wte_m.Tag:
        title = _('Could not export your tags to CSV file')
    elif model == wte_m.Contact:
        title = _('Could not export your contacts to CSV file')
    elif model == ta_m.Transaction:
        title = _('Could not export your transactions to CSV file')

    if return_render_or_file_as_http:
        context = {
            'title': title,
            'message': msg,
        }
        return render_or_file_as_http(request, csv_file_path, no_errors, context=context, content_type='text/csv')

    msg = msg + '. ' + title
    return csv_file_path, no_errors, msg
