# Author of Aqsa: Yulay Musin
from .forms import SignUpForm
from django.db.transaction import atomic as db_transaction_atomic
from . import models as m
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with db_transaction_atomic():
                form.save()
                m.Account.objects.create(user_id=form.instance.pk)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account:update_account')
    else:
        form = SignUpForm()
    return render(request=request, template_name='registration/signup.html', context={'form': form})
