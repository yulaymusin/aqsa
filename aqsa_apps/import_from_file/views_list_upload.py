# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from . import models as m
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView
from . import forms as f

from django.conf import settings

import zipfile
import os


class List(LoginRequiredMixin, mix.OwnerRequired, mix.ListViewContextLabelsPaginated):
    template_name = 'common/list.html'
    model = m.ImportFromFile
    model_labels_and_fields = ('date', 'checked', 'no_error', 'num_imported_rows', 'success',
                               'wallet', 'bank', 'variety')
    context = {
        'title': _('My Uploaded Files'),
        'links': (m.ImportFromFile.links['upload_bank_statement'], m.ImportFromFile.links['upload_backup_or_csv']),
        'msg_empty_object_list': _('You did not import any file. '
                                   'Click to "Upload Bank Statement" or "Upload Aqsa-Backup or CSV" for do that!'),
        'actions_description': _('Actions is not available if file contains any error or file was completely '
                                 'imported.'),
        'import_from_file': True,
    }


class UploadBankStatement(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs, FormView):
    success_url = None
    template_name = 'common/form.html'
    form_class = f.UploadBankStatementForm
    model = m.ImportFromFile
    context = {
        'title': _('Upload Bank Statement'),
        'links': (
            m.ImportFromFile.links['list'],
            m.ImportFromFile.links['upload_backup_or_csv'],
        ),
        'submit_btn': _('Upload'),
        'upload': True,
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.variety = 1
        form.save()
        self.success_url = form.instance.get_check_url()
        # User will be redirected to another software which will convert "wrong" TXT to okay CSV, then save new file
        # with original name in "MEDIA/import_from_file_sberbank/<user_id>" folder because folder of user not
        # "chmod 777" and PHP can not write to the folder of user. Finally redirect user to "get_check_url".
        if form.instance.bank == 'rub_sberbank' and not settings.DEBUG:
            self.success_url = '/sberbank.php?path=' + str(form.instance.file) + '&come_back=' + str(self.success_url)
            form.instance.file = 'import_from_file_sberbank' + form.instance.file[16:]
            form.save(update_fields=('file',))
        return super().form_valid(form)


class UploadBackupOrCSV(LoginRequiredMixin, mix.ContextForGenericView, FormView):
    success_url = None
    template_name = 'common/form.html'
    form_class = f.UploadBackupOrCSVForm
    model = m.ImportFromFile
    context = {
        'title': _('Upload Aqsa-backup or CSV file'),
        'links': (
            m.ImportFromFile.links['upload_bank_statement'],
            m.ImportFromFile.links['list'],
        ),
        'submit_btn': _('Upload'),
        'upload': True,
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        self.success_url = form.instance.get_check_url()

        # If user select the "Backup (All in one ZIP)"
        if form.instance.variety == 7:
            path_of_zip_file = form.instance.file.path

            no_error = False
            error_msg = _('Error! Your file is not the ZIP format file.')

            # If file is zipfile. Also can be checked extension of uploaded file.
            # or str(form.instance.file).split('.')[-1] == 'zip'
            if zipfile.is_zipfile(path_of_zip_file):
                unzip_to_path = os.path.join(
                    settings.MEDIA_ROOT, os.path.join('import_from_file', str(form.instance.pk)))

                fz = zipfile.ZipFile(path_of_zip_file, 'r')
                try:
                    fz.extract('wallets.csv', path=unzip_to_path)
                    fz.extract('categories.csv', path=unzip_to_path)
                    fz.extract('tags.csv', path=unzip_to_path)
                    fz.extract('contacts.csv', path=unzip_to_path)
                    fz.extract('transactions.csv', path=unzip_to_path)
                    no_error = True
                except KeyError:
                    error_msg = _('Error! Uploaded ZIP-file is not the back up file of Aqsa because it does'
                                  ' not contain required CSV-files.')
                    form.add_error('file', error_msg)
                    return super().form_invalid(form)
                finally:
                    fz.close()

                # Let's save space in our server. In any case, we do not need ZIP anymore.
                os.remove(path_of_zip_file)

            if no_error is False:
                form.add_error('file', error_msg)
                form.instance.delete()
                return super().form_invalid(form)

        return super().form_valid(form)
