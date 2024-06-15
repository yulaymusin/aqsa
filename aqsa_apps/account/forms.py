# Author of Aqsa: Yulay Musin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from . import models as m
from aqsa_apps import mixins as mix


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))
    first_name = forms.CharField(max_length=30, required=False, help_text=_('Optional.'))
    last_name = forms.CharField(max_length=30, required=False, help_text=_('Optional.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class AccountForm(forms.ModelForm):
    class Meta:
        model = m.Account
        exclude = ('user',)


class DeleteAccountForm(mix.FilterFieldsInFormByRequestUser, forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_('Type your password'))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_('Repeat your password'))
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label=_('Reason for deletion'), help_text=_('Tell us why do you want to delete your account.'))
    confirm = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        label=_('I have back up'), help_text=_('I exported my data from Aqsa and I am sure, '
                                               'I want to delete my account and all data of my account.'))

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            msg = _('You entered different passwords')
            self.add_error('password1', msg)
            self.add_error('password2', msg)
        else:
            valid = self.user.check_password(self.cleaned_data.get('password1'))
            if not valid:
                msg = _('You entered wrong password')
                self.add_error('password1', msg)
                self.add_error('password2', msg)
        return self.cleaned_data
