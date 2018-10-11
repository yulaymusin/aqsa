# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views as v


export_to_file_urlpatterns = [
    url(r'^home$', v.Home.as_view(), name='home'),

    url(r'^wallet_to_csv/(?P<filename>.*).csv', v.wallet_to_csv, name='wallet_to_csv'),
    url(r'^category_to_csv/(?P<filename>.*).csv', v.category_to_csv, name='category_to_csv'),
    url(r'^tag_to_csv/(?P<filename>.*).csv', v.tag_to_csv, name='tag_to_csv'),
    url(r'^contact_to_csv/(?P<filename>.*).csv', v.contact_to_csv, name='contact_to_csv'),
    url(r'^transaction_to_csv/(?P<filename>.*).csv', v.transaction_to_csv, name='transaction_to_csv'),

    url(r'^all_to_csv_and_zip/(?P<filename>.*).zip', v.all_to_csv_and_zip, name='all_to_csv_and_zip'),
]
