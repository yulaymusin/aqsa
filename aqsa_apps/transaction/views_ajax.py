# Author of Aqsa: Yulay Musin
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . import models as m
from . import forms as f
from django.utils.translation import ugettext as _
from django.http import HttpResponse
import json


@require_POST
@login_required
def ajax_update(request, pk):
    transaction = get_object_or_404(m.Transaction, pk=pk, owner=request.user)
    if transaction.transfer:
        form = f.EditAloneTransferForm(instance=transaction, data=request.POST or None, user=request.user)
    else:
        form = f.CreateEditIncomeExpenseForm(instance=transaction, data=request.POST or None, user=request.user)
    context = {'updated': '', 'errors': {}, 'msg': '', 'errors_in_fields': []}
    if form.is_valid():
        form.save()
        # example of response: {"updated": "yes", "errors": {},
        # "msg": "The transaction has been updated successfully", "errors_in_fields": []}
        context['updated'] = 'yes'
        context['msg'] = _('The transaction has been updated successfully')
    else:
        errors = {}
        errors_in_fields = []
        for field in form:
            if field.errors:
                errors_in_fields.append(str(field.name))
                errors_of_field = []
                for error in field.errors:
                    errors_of_field.append(error)
                errors[str(field.label)] = errors_of_field
        # example of response: {"updated": "no", "errors": {"Transfer": ["some err"], "Currency": ["some err"]}, "msg":
        # "The transaction has not been updated because of errors", "errors_in_fields": ["transfer", "currency"]}
        context['updated'] = 'no'
        context['errors'] = errors
        context['msg'] = _('The transaction has not been updated because of errors')
        context['errors_in_fields'] = errors_in_fields
    return HttpResponse(json.dumps(context))
