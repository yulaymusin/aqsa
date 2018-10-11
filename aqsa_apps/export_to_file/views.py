# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from . import viewxins as vx
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.transaction import models as ta_m
import random
import os
from django.conf import settings
import zipfile


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'export_to_file/home.html'

    def get_context_data(self, **kwargs):
        end_of_filename = _(' user')

        wallet_filename = _('Aqsa - list of wallets of ')
        wallet_filename = wallet_filename + self.request.user.get_full_name() + end_of_filename

        category_filename = _('Aqsa - list of categories of ')
        category_filename = category_filename + self.request.user.get_full_name() + end_of_filename

        tag_filename = _('Aqsa - list of tags of ')
        tag_filename = tag_filename + self.request.user.get_full_name() + end_of_filename

        contact_filename = _('Aqsa - list of contacts of ')
        contact_filename = contact_filename + self.request.user.get_full_name() + end_of_filename

        transaction_filename = _('Aqsa - list of transactions of ')
        transaction_filename = transaction_filename + self.request.user.get_full_name() + end_of_filename

        all_zip_filename = _('Aqsa - back up of ')
        all_zip_filename = all_zip_filename + self.request.user.get_full_name() + end_of_filename

        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Export data to file'),

            'wallet_to_csv_filename': wallet_filename,
            'category_to_csv_filename': category_filename,
            'tag_to_csv_filename': tag_filename,
            'contact_to_csv_filename': contact_filename,
            'transaction_to_csv_filename': transaction_filename,
            'all_to_csv_and_zip_filename': all_zip_filename,
        })
        return context


@login_required
def wallet_to_csv(request, filename):
    return vx.export_model_objects_to_csv(request, '', wte_m.Wallet, True)


@login_required
def category_to_csv(request, filename):
    return vx.export_model_objects_to_csv(request, '', wte_m.Category, True)


@login_required
def tag_to_csv(request, filename):
    return vx.export_model_objects_to_csv(request, '', wte_m.Tag, True)


@login_required
def contact_to_csv(request, filename):
    return vx.export_model_objects_to_csv(request, '', wte_m.Contact, True)


@login_required
def transaction_to_csv(request, filename):
    return vx.export_model_objects_to_csv(request, '', ta_m.Transaction, True)


@login_required
def all_to_csv_and_zip(request, filename):
    zip_file_name = 'user_' + str(request.user.id) + '_all_to_csv_and_zip_' + str(random.randint(1111, 9999)) + '.zip'
    zip_file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('export_to_file', zip_file_name))

    wallet_to_csv, no_error, msg = vx.export_model_objects_to_csv(request, '', wte_m.Wallet, False)
    if no_error:
        category_to_csv, no_error, msg = vx.export_model_objects_to_csv(request, '', wte_m.Category, False)
    if no_error:
        tag_to_csv, no_error, msg = vx.export_model_objects_to_csv(request, '', wte_m.Tag, False)
    if no_error:
        contact_to_csv, no_error, msg = vx.export_model_objects_to_csv(request, '', wte_m.Contact, False)
    if no_error:
        transaction_to_csv, no_error, msg = vx.export_model_objects_to_csv(request, '', ta_m.Transaction, False)
    if no_error:
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'export_to_file')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'export_to_file'))
        fz = zipfile.ZipFile(zip_file_path, 'w')  # создаем архив
        try:
            fz.write(wallet_to_csv, arcname='wallets.csv')
            fz.write(category_to_csv, arcname='categories.csv')
            fz.write(tag_to_csv, arcname='tags.csv')
            fz.write(contact_to_csv, arcname='contacts.csv')
            fz.write(transaction_to_csv, arcname='transactions.csv')

            # Let's save space in our server,
            os.remove(wallet_to_csv)
            os.remove(category_to_csv)
            os.remove(tag_to_csv)
            os.remove(contact_to_csv)
            os.remove(transaction_to_csv)
        finally:
            fz.close()
    context = {
        'title': _('Could not export your data'),
        'message': msg,
    }
    return vx.render_or_file_as_http(request, zip_file_path, no_error, context=context, content_type='application/zip')
