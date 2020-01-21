# Author of Aqsa: Yulay Musin
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy


class List(LoginRequiredMixin, mix.OwnerRequired, mix.ListViewContextLabelsPaginated):
    template_name = 'common/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'links': (self.model.links['create'],),
        })
        return context


class Create(LoginRequiredMixin, mix.ContextForGenericView, mix.MsgInFormValid,
             mix.SuccessUrl2ForCreateView, mix.TheSameNameErrorAndFormInstanceOwnerForCreateView, CreateView):

    template_name = 'common/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'submit_btn': _('Save'),
            'submit_btn2': _('Save and add another'),
            'links': (self.model.links['list'],),
        })
        return context


class Update(LoginRequiredMixin, mix.OwnerRequired, mix.ContextForGenericView, mix.MsgInFormValid, UpdateView):
    template_name = 'common/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'submit_btn': _('Save'),
            'submit_btn2': _('Save and continue editing'),
            'links': (self.model.links['list'], self.model.links['create'],),
        })
        return context

    def get_success_url(self):
        # If "Save and continue editing".
        if self.request.GET.get('success_url2'):
            self.success_url = reverse_lazy('wallet_tag_etc:wallet_edit', kwargs={'pk': self.kwargs.get('pk')})
        else:
            self.success_url = self.model.links['list'][0]
        return super().get_success_url()


class Delete(LoginRequiredMixin, mix.OwnerRequired, mix.DeleteViewWithProtectedErrOrSuccessMsgAndObjectsContext):
    template_name = 'common/confirm_delete_copy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'submit_btn': _('Yes, I am sure. Delete it!'),
            'links': (self.model.links['list'], self.model.links['create'],),
        })
        return context

    def get_success_url(self):
        self.success_url = self.model.links['list'][0]
        return super().get_success_url()
