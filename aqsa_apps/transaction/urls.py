# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views_lists as vl
from . import views_income_expense as vie
from . import views_transfer as vt
from . import views_ajax as ajax


# Lists of transactions.
transaction_urlpatterns = [
    url(r'^list$', vl.List.as_view(), name='list'),
    url(r'^list_filter$', vl.ListFilter.as_view(), name='list_filter'),
    url(r'^list_the_edit_mode$', vl.ListTheEditMode.as_view(), name='list_the_edit_mode'),
]

# Create, update, delete income/expense (NOT transfer).
transaction_urlpatterns += [
    url(r'^new_income_expense$', vie.Create.as_view(), name='new_income_expense'),
    url(r'^new_income_expense_set$', vie.create_set, name='new_income_expense_set'),
    url(r'^copy_transaction/(?P<pk>\d+)$', vie.copy_transaction, name='copy_transaction'),
    url(r'^edit_income_expense/(?P<pk>\d+)$', vie.Update.as_view(), name='edit_income_expense'),
    url(r'^delete/(?P<pk>\d+)$', vie.Delete.as_view(), name='delete'),
]

# Create, update, delete PAIR of transfer.
transaction_urlpatterns += [
    url(r'^new_pair_transfer$', vt.CreatePairTransfer.as_view(), name='new_pair_transfer'),
    url(r'^edit_pair_transfer/(?P<pk>\d+)$', vt.UpdatePairTransfer.as_view(), name='edit_pair_transfer'),
    url(r'^delete_pair_transfer/(?P<pk>\d+)$', vt.delete_pair_transfer, name='delete_pair_transfer'),
]

# AJAX.
transaction_urlpatterns += [
    url(r'^ajax_edit/(?P<pk>\d+)$', ajax.ajax_update, name='ajax_edit'),
]
