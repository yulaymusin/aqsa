# Author of Aqsa: Yulay Musin
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError


class OwnerRequired:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ContextForGenericView:
    context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(context, **self.context)


class ListViewContextPaginated:
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            try:
                paginate_by = int(self.request.GET.get('paginate_by'))
                # Will be better, if user will can't choose too big number, unless DB will work slow
                if paginate_by <= 100:
                    self.paginate_by = paginate_by
            except ValueError:
                pass
        return super().get_paginate_by(queryset)


class LabelsFieldsOfModelForGenericView:
    model_labels_and_fields = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = []
        for label in self.model_labels_and_fields:
            labels.append(self.model._meta.get_field(label).verbose_name)
        context['labels'] = labels
        context['fields'] = self.model_labels_and_fields
        return context


# This class just for group another classes.
class ListViewContextLabelsPaginated(ContextForGenericView, ListViewContextPaginated,
                                     LabelsFieldsOfModelForGenericView, ListView):
    pass


class DeleteViewWithProtectedErrOrSuccessMsgAndObjectsContext(ContextForGenericView, DeleteView):
    protected_error_msg = 'Could not delete this object because another object(s) linked to this object'
    success_message = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = (self.object,)
        return dict(context, **self.context)

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            return self.except_protected_error()

    def except_protected_error(self):
        context = self.get_context_data(object=self.object, except_protected_error=True)
        messages.error(self.request, self.protected_error_msg)
        return self.render_to_response(context)


class SuccessUrl2ForCreateView:
    success_url = None
    success_url2 = None

    def get_success_url(self):
        # If "Save and add another".
        if self.request.GET.get('success_url2') and self.success_url2:
            self.success_url = self.success_url2
        return super().get_success_url()


class TheSameNameErrorAndFormInstanceOwnerForCreateView:
    same_name_error_msg = 'You already have an object with the same name. ' \
                          'Do not get confused in the future, type another name'

    def form_valid(self, form):
        try:
            self.model.objects.get(owner=self.request.user, name=form.cleaned_data.get('name'))\
                .values_list('id', flat=True)
            form.add_error('name', self.same_name_error_msg)
            return super().form_invalid(form)
        except self.model.DoesNotExist:
            form.instance.owner = self.request.user
            return super().form_valid(form)


class MsgInFormValid:
    success_message = ''

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class RequestUserInGetFormKwargs:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class FilterFieldsInFormByRequestUser:
    filter_fields = ()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.filter_fields:
            self.fields[field].queryset = self.fields[field].queryset.filter(owner=self.user)
