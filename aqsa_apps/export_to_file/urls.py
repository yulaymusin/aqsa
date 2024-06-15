# Author of Aqsa: Yulay Musin
from django.urls import re_path
from . import views as v

app_name = 'export_to_file'

urlpatterns = [
    re_path(r'^home$', v.Home.as_view(), name='home'),

    re_path(r'^wallet_to_csv/(?P<filename>.*).csv', v.wallet_to_csv, name='wallet_to_csv'),
    re_path(r'^category_to_csv/(?P<filename>.*).csv', v.category_to_csv, name='category_to_csv'),
    re_path(r'^tag_to_csv/(?P<filename>.*).csv', v.tag_to_csv, name='tag_to_csv'),
    re_path(r'^contact_to_csv/(?P<filename>.*).csv', v.contact_to_csv, name='contact_to_csv'),
    re_path(r'^transaction_to_csv/(?P<filename>.*).csv', v.transaction_to_csv, name='transaction_to_csv'),

    re_path(r'^all_to_csv_and_zip/(?P<filename>.*).zip', v.all_to_csv_and_zip, name='all_to_csv_and_zip'),
]
