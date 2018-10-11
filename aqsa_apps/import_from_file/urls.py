# Author of Aqsa: Yulay Musin
from django.conf.urls import url

from . import views_list_upload as vlu

from .banks import rub_sberbank as rs
# from .banks import usd_bank as ub

from . import views_check_csv_backup as vccb
from . import views_db_records_csv_backup as vdrcb


# List of uploaded files and views for upload new files.
import_from_file_urlpatterns = [
    url(r'^list$', vlu.List.as_view(), name='list'),
    url(r'^upload_bank_statement$', vlu.UploadBankStatement.as_view(), name='upload_bank_statement'),
    url(r'^upload_backup_or_csv$', vlu.UploadBackupOrCSV.as_view(), name='upload_backup_or_csv'),
]


# <BANK STATEMENT
# rub_sberbank - Sberbank (Card in Russian Federation ruble currency).
import_from_file_urlpatterns += [
    url(r'^rub_sberbank_check/(?P<pk>\d+)$', rs.rub_sberbank_check, name='rub_sberbank_check'),
    url(r'^rub_sberbank_db_records/(?P<pk>\d+)$', rs.rub_sberbank_db_records, name='rub_sberbank_db_records'),  # check file and show errors if any error
]
# # usd_bank - Another Bank (Card in United States dollar currency).
# import_from_file_urlpatterns += [
#     url(r'^usd_bank_check/(?P<pk>\d+)$', ub.usd_bank_check, name='usd_bank_check'),
#     url(r'^usd_bank_db_records/(?P<pk>\d+)$', ub.usd_bank_db_records, name='usd_bank_db_records'),
# ]
# </BANK STATEMENT


# <CSV WITH WALLETS, CATEGORIES, TAGS, CONTACTS, TRANSACTIONS. BACKUP (ALL IN ONE ZIP)
# Check and confirm make records into DB.
import_from_file_urlpatterns += [
    url(r'^check_csv_wallets/(?P<pk>\d+)$', vccb.check_csv_wallets, name='check_csv_wallets'),
    url(r'^check_csv_categories/(?P<pk>\d+)$', vccb.check_csv_categories, name='check_csv_categories'),
    url(r'^check_csv_tags/(?P<pk>\d+)$', vccb.check_csv_tags, name='check_csv_tags'),
    url(r'^check_csv_contacts/(?P<pk>\d+)$', vccb.check_csv_contacts, name='check_csv_contacts'),
    url(r'^check_csv_transactions/(?P<pk>\d+)$', vccb.check_csv_transactions, name='check_csv_transactions'),
    url(r'^check_aqsa_backup/(?P<pk>\d+)$', vccb.check_aqsa_backup, name='check_aqsa_backup'),
]
# Make records into DB.
import_from_file_urlpatterns += [
    url(r'^db_records_csv_wallets/(?P<pk>\d+)$', vdrcb.db_records_csv_wallets, name='db_records_csv_wallets'),
    url(r'^db_records_csv_categories/(?P<pk>\d+)$', vdrcb.db_records_csv_categories, name='db_records_csv_categories'),
    url(r'^db_records_csv_tags/(?P<pk>\d+)$', vdrcb.db_records_csv_tags, name='db_records_csv_tags'),
    url(r'^db_records_csv_contacts/(?P<pk>\d+)$', vdrcb.db_records_csv_contacts, name='db_records_csv_contacts'),
    url(r'^db_records_csv_transactions/(?P<pk>\d+)$', vdrcb.db_records_csv_transactions,
        name='db_records_csv_transactions'),
    url(r'^db_records_aqsa_backup/(?P<pk>\d+)$', vdrcb.db_records_aqsa_backup, name='db_records_aqsa_backup'),
]
# </CSV WITH WALLETS, CATEGORIES, TAGS, CONTACTS, TRANSACTIONS. BACKUP (ALL IN ONE ZIP)
