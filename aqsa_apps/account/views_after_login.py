# Author of Aqsa: Yulay Musin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, render
from . import forms as f
from django.db.transaction import atomic as db_transaction_atomic
from django.utils.translation import activate
from . import models as m
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from aqsa_apps.about import models as ab_m
from aqsa_apps.transaction import models as ta_m
from django.views.generic import TemplateView


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your Password Was Changed'))
            return redirect('account:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'common/form.html', {
        'title': _('Change Password'),
        'submit_btn': _('Change Password'),
        'form': form
    })


@login_required
def update_account(request):
    if request.method == 'POST':
        user_form = f.UserForm(data=request.POST, instance=request.user)
        account_form = f.AccountForm(data=request.POST, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            with db_transaction_atomic():
                user_form.save()
                account_form.save()
            messages.success(request, _('Your Account Was Updated'))
            activate(request.user.account.language)
            return redirect('account:update_account')
    else:
        user_form = f.UserForm(instance=request.user)
        try:
            account_form = f.AccountForm(instance=request.user.account)
        except m.Account.DoesNotExist:
            m.Account.objects.create(user=request.user)
            account_form = f.AccountForm(instance=request.user.account)
    return render(request, 'common/form.html', {
        'title': _('Update Account'),
        'submit_btn': _('Update Account'),
        'form': user_form,
        'form2': account_form,
    })


class DeleteAccount(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs, FormView):
    form_class = f.DeleteAccountForm
    template_name = 'common/form.html'
    success_url = reverse_lazy('account:account_deleted')
    context = {
        'title': _('Delete Account'),
        'submit_btn': _('Delete Account'),
        'description': _('This action is irreversible'),
    }

    def form_valid(self, form):
        with db_transaction_atomic():
            ab_m.ReasonToDeleteAccount.objects.create(reason=form.cleaned_data.get('reason'))
            ta_m.Transaction.objects.filter(owner=self.request.user).delete()
            self.request.user.delete()
            messages.success(self.request, _('Your account was deleted'))
        return super().form_valid(form)


class AccountDeleted(mix.ContextForGenericView, TemplateView):
    template_name = 'account/account_deleted.html'
