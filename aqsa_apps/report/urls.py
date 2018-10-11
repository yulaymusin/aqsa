# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views_balance_of_category as vboc
from . import views_sum_of_income as vsoi
from . import views_sum_of_expense as vsoe


report_urlpatterns = []


# Views of report: Balance of every Category by the "Value in currency" (Sum Of Transactions, filtered by currency).
report_urlpatterns += [
    url(r'^balance_of_category_list$', vboc.List.as_view(), name='balance_of_category_list'),
    url(r'^balance_of_category_create$', vboc.Create.as_view(), name='balance_of_category_create'),
    url(r'^balance_of_category_read/(?P<pk>\d+)$', vboc.Read.as_view(), name='balance_of_category_read'),
]


# Views of report: Sum Of Income.
report_urlpatterns += [
    url(r'^sum_of_income_list$', vsoi.List.as_view(), name='sum_of_income_list'),
    url(r'^sum_of_income_create$', vsoi.Create.as_view(), name='sum_of_income_create'),
    url(r'^sum_of_income_read/(?P<pk>\d+)$', vsoi.Read.as_view(), name='sum_of_income_read'),
]


# Views of report: Sum Of Expense.
report_urlpatterns += [
    url(r'^sum_of_expense_list$', vsoe.List.as_view(), name='sum_of_expense_list'),
    url(r'^sum_of_expense_create$', vsoe.Create.as_view(), name='sum_of_expense_create'),
    url(r'^sum_of_expense_read/(?P<pk>\d+)$', vsoe.Read.as_view(), name='sum_of_expense_read'),
]
