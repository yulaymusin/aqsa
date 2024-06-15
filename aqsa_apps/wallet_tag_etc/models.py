# Author of Aqsa: Yulay Musin
from django.db import models
from django.contrib.auth.models import User
from . import validators as v
from django.utils.translation import gettext_lazy as _
from aqsa_apps.wallet_tag_etc import currencies
from django.urls import reverse_lazy


class Wallet(models.Model):
    class Meta:
        db_table = 'wallet'
        unique_together = ('owner', 'name')
        ordering = ('name',)

    # How many records will be added to DB per one "Wallet.objects.bulk_create()". Using in "import_from_file"
    MAX_NUM_OF_RECORDS_PER_BULK = 50

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50, validators=[v.two_or_more_spaces], verbose_name=_('Name'))
    currency = models.PositiveSmallIntegerField(choices=currencies.ISO_4217_CURRENCIES, verbose_name=_('Currency'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse_lazy('wallet_tag_etc:wallet_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('wallet_tag_etc:wallet_delete', kwargs={'pk': self.pk})

    def get_currency_title(self):
        return currencies.get_currency_title(self.currency)

    links = {
        'create': (reverse_lazy('wallet_tag_etc:wallet_new'), _('New Wallet'), 'fas fa-file-signature'),
        'list': (reverse_lazy('wallet_tag_etc:wallet_list'), _('List of Wallets'), 'fas fa-list-ul'),
    }


class Category(models.Model):
    class Meta:
        db_table = 'category'
        unique_together = ('owner', 'name')
        ordering = ('name',)

    MAX_NUM_OF_RECORDS_PER_BULK = 50

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50, validators=[v.two_or_more_spaces], verbose_name=_('Name'))

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse_lazy('wallet_tag_etc:category_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('wallet_tag_etc:category_delete', kwargs={'pk': self.pk})

    links = {
        'create': (reverse_lazy('wallet_tag_etc:category_new'), _('New Category'), 'fas fa-file-signature'),
        'list': (reverse_lazy('wallet_tag_etc:category_list'), _('List of Categories'), 'fas fa-list-ul'),
    }


class Tag(models.Model):
    class Meta:
        db_table = 'tag'
        unique_together = ('owner', 'name')
        ordering = ('name',)

    MAX_NUM_OF_RECORDS_PER_BULK = 50

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50, validators=[v.reserved_symbol, v.two_or_more_spaces], verbose_name=_('Name'))

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse_lazy('wallet_tag_etc:tag_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('wallet_tag_etc:tag_delete', kwargs={'pk': self.pk})

    links = {
        'create': (reverse_lazy('wallet_tag_etc:tag_new'), _('New Tag'), 'fas fa-file-signature'),
        'list': (reverse_lazy('wallet_tag_etc:tag_list'), _('List of Tags'), 'fas fa-list-ul'),
    }


class Contact(models.Model):
    class Meta:
        db_table = 'contact'
        unique_together = ('owner', 'name')
        ordering = ('name',)

    MAX_NUM_OF_RECORDS_PER_BULK = 50

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50, validators=[v.two_or_more_spaces], verbose_name=_('Name'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse_lazy('wallet_tag_etc:contact_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('wallet_tag_etc:contact_delete', kwargs={'pk': self.pk})

    links = {
        'create': (reverse_lazy('wallet_tag_etc:contact_new'), _('New Contact'), 'fas fa-file-signature'),
        'list': (reverse_lazy('wallet_tag_etc:contact_list'), _('List of Contacts'), 'fas fa-list-ul'),
    }
