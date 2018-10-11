# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views_category as category, views_contact as contact, views_tag as tag, views_wallet as wallet

wallet_tag_etc_urlpatterns = [
    url(r'^wallet/list$', wallet.List.as_view(), name='wallet_list'),
    url(r'^wallet/new$', wallet.Create.as_view(), name='wallet_new'),
    url(r'^wallet/edit/(?P<pk>\d+)$', wallet.Update.as_view(), name='wallet_edit'),
    url(r'^wallet/delete/(?P<pk>\d+)$', wallet.Delete.as_view(), name='wallet_delete'),

    url(r'^category/list$', category.List.as_view(), name='category_list'),
    url(r'^category/new$', category.Create.as_view(), name='category_new'),
    url(r'^category/edit/(?P<pk>\d+)$', category.Update.as_view(), name='category_edit'),
    url(r'^category/delete/(?P<pk>\d+)$', category.Delete.as_view(), name='category_delete'),

    url(r'^tag/list$', tag.List.as_view(), name='tag_list'),
    url(r'^tag/new$', tag.Create.as_view(), name='tag_new'),
    url(r'^tag/edit/(?P<pk>\d+)$', tag.Update.as_view(), name='tag_edit'),
    url(r'^tag/delete/(?P<pk>\d+)$', tag.Delete.as_view(), name='tag_delete'),

    url(r'^contact/list$', contact.List.as_view(), name='contact_list'),
    url(r'^contact/new$', contact.Create.as_view(), name='contact_new'),
    url(r'^contact/edit/(?P<pk>\d+)$', contact.Update.as_view(), name='contact_edit'),
    url(r'^contact/delete/(?P<pk>\d+)$', contact.Delete.as_view(), name='contact_delete'),
]
