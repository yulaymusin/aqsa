# Author of Aqsa: Yulay Musin
from django.urls import re_path
from . import views_lists as vl
from . import views_income_expense as vie
from . import views_transfer as vt
from . import views_ajax as ajax

app_name = 'transaction'

# Lists of transactions.
urlpatterns = [
    re_path(r'^list$', vl.List.as_view(), name='list'),
    re_path(r'^list_filter$', vl.ListFilter.as_view(), name='list_filter'),
    re_path(r'^list_the_edit_mode$', vl.ListTheEditMode.as_view(), name='list_the_edit_mode'),
]

# Create, update, delete income/expense (NOT transfer).
urlpatterns += [
    re_path(r'^new_income_expense$', vie.Create.as_view(), name='new_income_expense'),
    re_path(r'^new_income_expense_set$', vie.create_set, name='new_income_expense_set'),
    re_path(r'^copy_transaction/(?P<pk>\d+)$', vie.copy_transaction, name='copy_transaction'),
    re_path(r'^edit_income_expense/(?P<pk>\d+)$', vie.Update.as_view(), name='edit_income_expense'),
    re_path(r'^delete/(?P<pk>\d+)$', vie.Delete.as_view(), name='delete'),
]

# Create, update, delete PAIR of transfer.
urlpatterns += [
    re_path(r'^new_pair_transfer$', vt.CreatePairTransfer.as_view(), name='new_pair_transfer'),
    re_path(r'^edit_pair_transfer/(?P<pk>\d+)$', vt.UpdatePairTransfer.as_view(), name='edit_pair_transfer'),
    re_path(r'^delete_pair_transfer/(?P<pk>\d+)$', vt.delete_pair_transfer, name='delete_pair_transfer'),
]

# AJAX.
urlpatterns += [
    re_path(r'^ajax_edit/(?P<pk>\d+)$', ajax.ajax_update, name='ajax_edit'),
]
