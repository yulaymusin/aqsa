# Author of Aqsa: Yulay Musin
from . import viewxins_mixins as vxmx
from . import models as m
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy


class List(vxmx.List):
    model = m.Tag
    model_labels_and_fields = ('name',)
    context = {
        'title': _('Tags'),
        'msg_empty_object_list': _('You do not have any tag. Click to "New Tag" button for create it!'),
    }


class Create(vxmx.Create):
    model = m.Tag
    fields = ['name']

    success_url = reverse_lazy('wallet_tag_etc:tag_list')
    success_url2 = reverse_lazy('wallet_tag_etc:tag_new')

    success_message = _('Tag have been created.')
    same_name_error_msg = _('You already have a tag with the same name. '
                            'Do not get confused in the future, type another name')
    context = {
        'title': _('New Tag'),
    }


class Update(vxmx.Update):
    model = m.Tag
    fields = ['name']
    success_message = _('The tag was updated.')
    context = {
        'title': _('Edit Tag'),
    }


class Delete(vxmx.Delete):
    model = m.Tag
    success_message = _('The tag was deleted.')
    context = {
        'title': _('Delete Tag'),
        'description': _('Are you sure you want to delete the tag shown below?'),
        'labels': [m.Tag._meta.get_field(label).verbose_name for label in List.model_labels_and_fields],
        'fields': List.model_labels_and_fields,
    }
