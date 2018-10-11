# Author of Aqsa: Yulay Musin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from . import validators as v
from aqsa_apps.wallet_tag_etc import models as wallet_tag_etc_m
from django.core.urlresolvers import reverse_lazy


def upload_to(instance, filename):
    return 'import_from_file/{0}/{1}'.format(instance.owner.id, filename)


class ImportFromFile(models.Model):
    class Meta:
        db_table = 'import_from_file'
        ordering = ('-date', '-pk')

    varieties = (
        (1, _('Bank Statement')),
        (2, _('CSV with Wallets')),
        (3, _('CSV with Categories')),
        (4, _('CSV with Tags')),
        (5, _('CSV with Contacts')),
        (6, _('CSV with Transactions')),
        (7, _('Backup (All in one ZIP)')),
    )

    available_banks = (
        # bank statement of main bank of the RF (Russian Federation)
        ('rub_sberbank', _('Sberbank (Card in Russian Federation ruble currency)')),
        # TO DO: ('usd_bank', _('Another Bank (Card in United States dollar currency)')),
    )

    owner = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    file = models.FileField(
        upload_to=upload_to, validators=[v.file_size, v.file_extension], verbose_name=_('File'))

    checked = models.BooleanField(default=False, verbose_name=_('Checked'))
    no_error = models.NullBooleanField(verbose_name=_('No error'))
    num_imported_rows = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('* Number of imported rows'))
    success = models.BooleanField(default=False, verbose_name=_('Import finished successfully'))

    wallet = models.ForeignKey(wallet_tag_etc_m.Wallet, null=True, verbose_name=_('Wallet'))
    bank = models.CharField(max_length=20, choices=available_banks, null=True, verbose_name=_('Bank'))

    variety = models.PositiveSmallIntegerField(choices=varieties, verbose_name=_('Variety of uploaded file'))

    def __str__(self):
        return str(self.file)

    def get_bank_name(self):
        for ba in self.available_banks:
            if ba[0] == self.bank:
                return ba[1]

    def get_variety_name(self):
        for va in self.varieties:
            if va[0] == self.variety:
                return va[1]

    def mark_as_checked(self, no_error):
        self.checked = True
        self.no_error = no_error
        self.save(update_fields=('checked', 'no_error'))

    def mark_as_finished(self):
        self.success = True
        self.save(update_fields=('success',))

    parts_of_urls = {
        2: 'csv_wallets',
        3: 'csv_categories',
        4: 'csv_tags',
        5: 'csv_contacts',
        6: 'csv_transactions',
        7: 'aqsa_backup',
    }

    def get_check_url(self):
        if self.variety == 1:
            reverse_url = 'import_from_file:' + str(self.bank) + '_check'
        else:
            reverse_url = 'import_from_file:check_' + self.parts_of_urls[self.variety]
        return reverse_lazy(reverse_url, kwargs={'pk': self.pk})

    def get_db_records_url(self):
        if self.variety == 1:
            reverse_url = 'import_from_file:' + str(self.bank) + '_db_records'
        else:
            reverse_url = 'import_from_file:db_records_' + self.parts_of_urls[self.variety]
        return reverse_lazy(reverse_url, kwargs={'pk': self.pk})

    links = {
        'upload_bank_statement': (
            reverse_lazy('import_from_file:upload_bank_statement'), _('Upload Bank Statement'), 'fas fa-money-check'),
        'upload_backup_or_csv': (
            reverse_lazy('import_from_file:upload_backup_or_csv'), _('Upload Aqsa-Backup or CSV'),
            'fas fa-file-archive'),
        'list': (reverse_lazy('import_from_file:list'), _('List of Imported Files'), 'fas fa-list-ul'),
    }
