# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from django.views.generic.edit import CreateView, UpdateView
from . import forms as f
from . import models as m
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.forms.models import formset_factory
from django.db.transaction import atomic as db_transaction_atomic
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from .views_lists import List as vie_List


class Create(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs, mix.MsgInFormValid,
             mix.SuccessUrl2ForCreateView, CreateView):

    template_name = 'common/form.html'
    form_class = f.CreateEditIncomeExpenseForm
    model = m.Transaction

    success_url = reverse_lazy('transaction:list')
    success_url2 = reverse_lazy('transaction:new_income_expense')

    success_message = _('Transaction have been created.')

    context = {
        'title': _('New Transaction (Income or Expense)'),
        'submit_btn': _('Save'),
        'submit_btn2': _('Save and add another'),
        'links': (
            m.Transaction.links['list'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
        'datetimepicker': True,
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def create_set(request):
    def get_formset(request, extra):
        formset = formset_factory(form=f.CreateEditIncomeExpenseForm, max_num=15, extra=extra)
        form_kwargs = {'user': request.user}
        if request.POST:
            return formset(request.POST, form_kwargs=form_kwargs)
        return formset(form_kwargs=form_kwargs)

    extra = 2
    if request.GET.get('extra'):
        try:
            extra = int(request.GET.get('extra'))
        except ValueError:
            pass

    formset = get_formset(request, extra)

    if request.method == 'POST':
        if formset.is_valid():
            with db_transaction_atomic():
                for form in formset:
                    form.instance.owner = request.user
                    form.save()
            messages.success(request, _('Transactions have been created.'))
            return redirect(reverse_lazy('transaction:list'))
    return render(request=request, template_name='transaction/new_set.html', context={
        'form': f.CreateEditIncomeExpenseForm,
        'formset': formset,
        'title': _('New Set (Income or Expense)'),
        'extra': extra,
        'datetimepicker': True,
        'links': (
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['list'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
    })


@login_required
def copy_transaction(request, pk):
    transaction = get_object_or_404(m.Transaction, pk=pk, owner=request.user, transfer=False)
    if request.method == 'POST':
        tags_for_transaction = [tag for tag in transaction.tag.all()]
        transaction.pk = None
        with db_transaction_atomic():
            transaction.save()
            transaction.tag.add(*tags_for_transaction)
        messages.success(request, _('The transaction was copied.'))
        return redirect(reverse_lazy('transaction:list'))

    model_labels_and_fields = vie_List.model_labels_and_fields

    return render(request=request, template_name='common/confirm_delete_copy.html', context={
        'title': _('Make copy of existing transaction'),
        'description': _('Are you sure you want to make a copy of the following transaction?'),
        'submit_btn': _('Make copy'),
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
        'objects': (transaction,),
    })


class Update(LoginRequiredMixin, mix.OwnerRequired, mix.ContextForGenericView, mix.MsgInFormValid,
             mix.RequestUserInGetFormKwargs, UpdateView):
    template_name = 'common/form.html'
    model = m.Transaction
    form_class = f.CreateEditIncomeExpenseForm  # fields =

    success_message = _('The transaction was updated.')

    context = {
        'title': _('Edit Transaction (Income or Expense)'),
        'submit_btn': _('Save'),
        'submit_btn2': _('Save and continue editing'),
        'links': (
            m.Transaction.links['list'],
            m.Transaction.links['new_income_expense'],
            m.Transaction.links['new_pair_transfer'],
            m.Transaction.links['new_income_expense_set'],
            m.Transaction.links['list_filter'],
            m.Transaction.links['list_the_edit_mode'],
        ),
        'datetimepicker': True,
    }

    def get_queryset(self):
        return super().get_queryset().filter(transfer=False)

    def get_success_url(self):
        # if "Save and continue editing"
        if self.request.GET.get('success_url2'):
            return reverse_lazy('transaction:edit_income_expense', kwargs={'pk': self.kwargs.get('pk')})
        return reverse_lazy('transaction:list')


class Delete(LoginRequiredMixin, mix.OwnerRequired, mix.DeleteViewWithProtectedErrOrSuccessMsgAndObjectsContext):
    template_name = 'common/confirm_delete_copy.html'
    model = m.Transaction
    success_url = reverse_lazy('transaction:list')
    success_message = _('The transaction was deleted.')
    context = {
        'title': _('Delete Transaction'),
        'description': _('Are you sure you want to delete the transaction shown below?'),
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

        'labels': [m.Transaction._meta.get_field(label).verbose_name for label in vie_List.model_labels_and_fields],
        'fields': vie_List.model_labels_and_fields,
    }

    def get_queryset(self):
        return super().get_queryset().select_related('wallet', 'category', 'contact').prefetch_related('tag')
