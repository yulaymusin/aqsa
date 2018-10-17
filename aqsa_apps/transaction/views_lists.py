# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from . import models as m
from django.utils.translation import ugettext_lazy as _
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps.wallet_tag_etc import currencies


class List(LoginRequiredMixin, mix.OwnerRequired, mix.ListViewContextLabelsPaginated):
    template_name = 'common/list.html'
    model = m.Transaction
    model_labels_and_fields = ('transfer', 'date', 'value', 'wallet', 'category', 'description', 'tag',
                               'currency', 'value_in_curr', 'contact', 'not_ignore', 'bank_date', 'bank_ta_id')
    context = {
        'title': _('My Transactions'),
        'links': (
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
        'msg_empty_object_list': _('You do not have any transaction. Click to one of "New..." button '
                                   'for create it!'),
        'transaction': True,
    }

    def get_queryset(self):
        return super().get_queryset().select_related('wallet', 'category', 'contact').prefetch_related('tag')


# TODO: add more filters
class ListFilter(List):
    model_labels_and_fields = List.model_labels_and_fields

    transfer = None
    wallet = None
    category = None
    tag = None
    currency = None
    contact = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transfer_filter'] = self.transfer
        context['wallet_filter'] = self.wallet
        context['category_filter'] = self.category
        context['tag_filter'] = self.tag
        context['currency_filter'] = self.currency
        context['contact_filter'] = self.contact

        context['titles_of_labels'] = dict((label, m.Transaction._meta.get_field(label).verbose_name) for label in
                                           ('transfer', 'wallet', 'category', 'tag', 'currency', 'contact'))

        context['title'] = _('Search Transactions')

        context['msg_empty_object_list'] = _('Nothing found by applied filters')

        context['wallet'] = wte_m.Wallet.objects.filter(owner=self.request.user)
        context['category'] = wte_m.Category.objects.filter(owner=self.request.user)
        context['tag'] = wte_m.Tag.objects.filter(owner=self.request.user)
        context['currency'] = currencies.ISO_4217_CURRENCIES
        context['contact'] = wte_m.Contact.objects.filter(owner=self.request.user)

        context['links'] = (
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list'],
            m.Transaction.links['list_the_edit_mode'],
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        transfer = self.request.GET.get('transfer')
        wallet = self.request.GET.get('wallet')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        currency = self.request.GET.get('currency')
        contact = self.request.GET.get('contact')

        if transfer == 'True':
            qs = qs.filter(transfer=True)
            self.transfer = True
        elif transfer == 'False':
            qs = qs.filter(transfer=False)
            self.transfer = False

        try:
            if wallet:
                qs = qs.filter(wallet=int(wallet))
                self.wallet = int(wallet)
        except ValueError:
            pass

        try:
            if category:
                qs = qs.filter(category=int(category))
                self.category = int(category)
        except ValueError:
            pass

        try:
            if tag:
                qs = qs.filter(tag=int(tag))
                self.tag = int(tag)
        except ValueError:
            pass

        try:
            if currency:
                qs = qs.filter(currency=int(currency))
                self.currency = int(currency)
        except ValueError:
            pass

        try:
            if contact:
                qs = qs.filter(contact=int(contact))
                self.contact = int(contact)
        except ValueError:
            pass

        return qs


class ListTheEditMode(ListFilter):
    template_name = 'transaction/list_the_edit_mode.html'
    model_labels_and_fields = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('Edit Transactions')
        context['datetimepicker'] = True

        titles_of_thead = List.model_labels_and_fields
        context['titles_of_thead'] = dict((label, m.Transaction._meta.get_field(label).verbose_name) for label in
                                          titles_of_thead)

        context['titles_of_labels'] = None

        context['links'] = (
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list'],
        )
        return context
