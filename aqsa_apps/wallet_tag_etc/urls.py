# Author of Aqsa: Yulay Musin
from django.urls import re_path
from . import views_category as category, views_contact as contact, views_tag as tag, views_wallet as wallet

app_name = 'wallet_tag_etc'

urlpatterns = [
    re_path(r'^wallet/list$', wallet.List.as_view(), name='wallet_list'),
    re_path(r'^wallet/new$', wallet.Create.as_view(), name='wallet_new'),
    re_path(r'^wallet/edit/(?P<pk>\d+)$', wallet.Update.as_view(), name='wallet_edit'),
    re_path(r'^wallet/delete/(?P<pk>\d+)$', wallet.Delete.as_view(), name='wallet_delete'),

    re_path(r'^category/list$', category.List.as_view(), name='category_list'),
    re_path(r'^category/new$', category.Create.as_view(), name='category_new'),
    re_path(r'^category/edit/(?P<pk>\d+)$', category.Update.as_view(), name='category_edit'),
    re_path(r'^category/delete/(?P<pk>\d+)$', category.Delete.as_view(), name='category_delete'),

    re_path(r'^tag/list$', tag.List.as_view(), name='tag_list'),
    re_path(r'^tag/new$', tag.Create.as_view(), name='tag_new'),
    re_path(r'^tag/edit/(?P<pk>\d+)$', tag.Update.as_view(), name='tag_edit'),
    re_path(r'^tag/delete/(?P<pk>\d+)$', tag.Delete.as_view(), name='tag_delete'),

    re_path(r'^contact/list$', contact.List.as_view(), name='contact_list'),
    re_path(r'^contact/new$', contact.Create.as_view(), name='contact_new'),
    re_path(r'^contact/edit/(?P<pk>\d+)$', contact.Update.as_view(), name='contact_edit'),
    re_path(r'^contact/delete/(?P<pk>\d+)$', contact.Delete.as_view(), name='contact_delete'),
]
