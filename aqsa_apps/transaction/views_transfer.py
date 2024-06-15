# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from django.views.generic.edit import FormView
from . import forms as f
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from . import models as m
from django.db.transaction import atomic as db_transaction_atomic
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_lists import List as vie_List


class CreatePairTransfer(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs,
                         mix.SuccessUrl2ForCreateView, FormView):
    template_name = 'common/form.html'
    form_class = f.CreateEditPairTransferForm
    context = {
        'title': _('New Transactions (Pair of Money Transfer)'),
        'description': _('This form will create two transactions. #1 - fill positive value and choose wallet to '
                         'which receive the money, #2 - fill negative value and choose wallet from which the money '
                         'goes'),
        'submit_btn': _('Save'),
        'submit_btn2': _('Save and add another'),
        'links': (
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['list'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_the_edit_mode'],
            m.Transaction.links['list_filter'],
        ),
        'datetimepicker': True,
    }
    success_url = reverse_lazy('transaction:list')
    success_url2 = reverse_lazy('transaction:new_pair_transfer')

    def form_valid(self, form):
        fcd = form.cleaned_data

        ta1 = m.Transaction(
            owner=self.request.user,
            transfer=True,
            date=fcd.get('date'),
            value=fcd.get('value1'),
            wallet=fcd.get('wallet1'),
            category=fcd.get('category'),
            description=fcd.get('description1'),
            # tag below
            currency=fcd.get('currency'),
            value_in_curr=fcd.get('value_in_curr'),
            contact=fcd.get('contact'),
            bank_date=fcd.get('bank_date1'),
            bank_ta_id=fcd.get('bank_ta_id1'),
        )
        ta2 = m.Transaction(
            owner=self.request.user,
            transfer=True,
            date=ta1.date,
            value=fcd.get('value2'),
            wallet=fcd.get('wallet2'),
            category=ta1.category,
            description=fcd.get('description2'),
            # tag below
            currency=ta1.currency,
            value_in_curr=ta1.value_in_curr * -1,
            contact=ta1.contact,
            bank_date=fcd.get('bank_date2'),
            bank_ta_id=fcd.get('bank_ta_id2'),
        )
        tags_for_ta1 = [tag1 for tag1 in fcd.get('tag1')]
        tags_for_ta2 = [tag2 for tag2 in fcd.get('tag2')]

        with db_transaction_atomic():
            ta1.save()
            ta2.transfer_related = ta1
            ta2.save()

            ta1.tag.add(*tags_for_ta1)
            ta2.tag.add(*tags_for_ta2)

        messages.success(self.request, _('Transactions (Pair of Money Transfer) have been created.'))
        return super().form_valid(form)


class UpdatePairTransfer(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs, FormView):
    template_name = 'common/form.html'
    form_class = f.CreateEditPairTransferForm
    context = {
        'title': _('Edit Transactions (Pair of Money Transfer)'),
        'submit_btn': _('Save'),
        'submit_btn2': _('Save and continue editing'),
        'datetimepicker': True,
        'links': (
            m.Transaction.links['list'],
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
    }

    ta1 = None
    ta2 = None

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        ta = get_object_or_404(
            m.Transaction.objects.select_related('transfer_related', 'wallet').prefetch_related('tag'),
            owner=self.request.user, transfer=True, pk=pk
        )
        if ta.transfer_related:
            self.ta1 = ta.transfer_related
            self.ta2 = ta
        else:
            self.ta1 = ta
            self.ta2 = get_object_or_404(m.Transaction.objects.select_related('transfer_related', 'wallet'),
                                         owner=self.request.user, transfer=True, transfer_related=ta)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial = {
            'date': self.ta1.date,

            'value1': self.ta1.value,
            'value2': self.ta2.value,

            'wallet1': self.ta1.wallet,
            'wallet2': self.ta2.wallet,

            'category': self.ta1.category,

            'description1': self.ta1.description,
            'description2': self.ta2.description,

            'tag1': [t1 for t1 in self.ta1.tag.all()],
            'tag2': [t2 for t2 in self.ta2.tag.all()],

            'currency': self.ta1.currency,
            'value_in_curr': self.ta1.value_in_curr,
            'contact': self.ta1.contact,

            'bank_date1': self.ta1.bank_date,
            'bank_date2': self.ta2.bank_date,

            'bank_ta_id1': self.ta1.bank_ta_id,
            'bank_ta_id2': self.ta2.bank_ta_id,
        }
        return super().get_initial()

    def form_valid(self, form):
        # ManyToMany objects for add and for remove.
        def mtm_objects_for_add_and_remove(old_set, new_set):
            should_be_removed = []
            for obj in old_set:
                # If existing tag does not exists in new set of tags, then it should be removed
                if obj not in new_set:
                    should_be_removed.append(obj)

            should_be_added = []
            for obj in new_set:
                # If new tag does not exists in existing set of tags, then it should be added
                if obj not in old_set:
                    should_be_added.append(obj)

            return should_be_added, should_be_removed

        fcd = form.cleaned_data

        self.ta1.date = fcd.get('date')
        self.ta1.value = fcd.get('value1')
        self.ta1.wallet = fcd.get('wallet1')
        self.ta1.category = fcd.get('category')
        self.ta1.description = fcd.get('description1')
        # tag below
        self.ta1.currency = fcd.get('currency')
        self.ta1.value_in_curr = fcd.get('value_in_curr')
        self.ta1.contact = fcd.get('contact')
        self.ta1.bank_date = fcd.get('bank_date1')
        self.ta1.bank_ta_id = fcd.get('bank_ta_id1')

        self.ta2.date = self.ta1.date
        self.ta2.value = fcd.get('value2')
        self.ta2.wallet = fcd.get('wallet2')
        self.ta2.category = self.ta1.category
        self.ta2.description = fcd.get('description2')
        # tag below
        self.ta2.currency = self.ta1.currency
        self.ta2.value_in_curr = self.ta1.value_in_curr * -1
        self.ta2.contact = self.ta1.contact
        self.ta2.bank_date = fcd.get('bank_date2')
        self.ta2.bank_ta_id = fcd.get('bank_ta_id2')

        ta1_tags_add, ta1_tags_rmv = mtm_objects_for_add_and_remove(self.ta1.tag.all(), fcd.get('tag1'))
        ta2_tags_add, ta2_tags_rmv = mtm_objects_for_add_and_remove(self.ta2.tag.all(), fcd.get('tag2'))

        with db_transaction_atomic():
            self.ta1.save(update_fields=('date', 'value', 'wallet', 'category', 'description',
                                         'currency', 'value_in_curr', 'contact', 'bank_date', 'bank_ta_id'))
            self.ta2.save(update_fields=('date', 'value', 'wallet', 'category', 'description',
                                         'currency', 'value_in_curr', 'contact', 'bank_date', 'bank_ta_id'))
            self.ta1.tag.add(*ta1_tags_add)
            self.ta2.tag.add(*ta2_tags_add)
            self.ta1.tag.remove(*ta1_tags_rmv)
            self.ta2.tag.remove(*ta2_tags_rmv)

        messages.success(self.request, _('Transactions (Pair of Money Transfer) was updated.'))
        return super().form_valid(form)

    def get_success_url(self):
        # if "Save and continue editing"
        if self.request.GET.get('success_url2'):
            return reverse_lazy('transaction:edit_pair_transfer', kwargs={'pk': self.kwargs.get('pk')})
        return reverse_lazy('transaction:list')


@login_required
def delete_pair_transfer(request, pk):
    ta = get_object_or_404(m.Transaction.objects.select_related('transfer_related', 'wallet').prefetch_related('tag'),
                           owner=request.user, transfer=True, pk=pk)
    if ta.transfer_related:
        ta1 = ta.transfer_related
        ta2 = ta
    else:
        ta1 = ta
        ta2 = get_object_or_404(m.Transaction.objects.select_related('transfer_related', 'wallet'),
                                owner=request.user, transfer=True, transfer_related=ta)

    if request.method == 'POST':
        with db_transaction_atomic():
            # TODO: Why Django/PostgreSQL want to remove one of transactions twice?
            ta1.delete()
            ta2.delete()
        messages.success(request, _('Transactions (Pair of Money Transfer) was deleted.'))
        return redirect(reverse_lazy('transaction:list'))

    model_labels_and_fields = vie_List.model_labels_and_fields

    return render(request=request, template_name='common/confirm_delete_copy.html', context={
        'title': _('Delete Transactions (Pair of Money Transfer)'),
        'description': _('Are you sure you want to delete the transactions shown below?'),
        'submit_btn': _('Yes, I am sure. Delete it!'),
        'links': (
            m.Transaction.links['list'],
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
        'transaction': True,

        'labels': [m.Transaction._meta.get_field(label).verbose_name for label in model_labels_and_fields],
        'fields': model_labels_and_fields,
        'objects': (ta1, ta2),
    })
