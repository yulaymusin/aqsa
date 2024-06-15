# Author of Aqsa: Yulay Musin
from django.urls import re_path

from . import views_list_upload as vlu

from . import views_check_csv_backup as vccb
from . import views_db_records_csv_backup as vdrcb

app_name = 'import_from_file'

# List of uploaded files and views for upload new files.
urlpatterns = [
    re_path(r'^list$', vlu.List.as_view(), name='list'),
    re_path(r'^upload_bank_statement$', vlu.UploadBankStatement.as_view(), name='upload_bank_statement'),
    re_path(r'^upload_backup_or_csv$', vlu.UploadBackupOrCSV.as_view(), name='upload_backup_or_csv'),
]


# <BANK STATEMENT
# # usd_bank - Another Bank (Card in United States dollar currency).
# import_from_file_urlpatterns += [
#     re_path(r'^usd_bank_check/(?P<pk>\d+)$', ub.usd_bank_check, name='usd_bank_check'),
#     re_path(r'^usd_bank_db_records/(?P<pk>\d+)$', ub.usd_bank_db_records, name='usd_bank_db_records'),
# ]
# </BANK STATEMENT


# <CSV WITH WALLETS, CATEGORIES, TAGS, CONTACTS, TRANSACTIONS. BACKUP (ALL IN ONE ZIP)
# Check and confirm make records into DB.
urlpatterns += [
    re_path(r'^check_csv_wallets/(?P<pk>\d+)$', vccb.check_csv_wallets, name='check_csv_wallets'),
    re_path(r'^check_csv_categories/(?P<pk>\d+)$', vccb.check_csv_categories, name='check_csv_categories'),
    re_path(r'^check_csv_tags/(?P<pk>\d+)$', vccb.check_csv_tags, name='check_csv_tags'),
    re_path(r'^check_csv_contacts/(?P<pk>\d+)$', vccb.check_csv_contacts, name='check_csv_contacts'),
    re_path(r'^check_csv_transactions/(?P<pk>\d+)$', vccb.check_csv_transactions, name='check_csv_transactions'),
    re_path(r'^check_aqsa_backup/(?P<pk>\d+)$', vccb.check_aqsa_backup, name='check_aqsa_backup'),
]
# Make records into DB.
urlpatterns += [
    re_path(r'^db_records_csv_wallets/(?P<pk>\d+)$', vdrcb.db_records_csv_wallets, name='db_records_csv_wallets'),
    re_path(r'^db_records_csv_categories/(?P<pk>\d+)$', vdrcb.db_records_csv_categories, name='db_records_csv_categories'),
    re_path(r'^db_records_csv_tags/(?P<pk>\d+)$', vdrcb.db_records_csv_tags, name='db_records_csv_tags'),
    re_path(r'^db_records_csv_contacts/(?P<pk>\d+)$', vdrcb.db_records_csv_contacts, name='db_records_csv_contacts'),
    re_path(r'^db_records_csv_transactions/(?P<pk>\d+)$', vdrcb.db_records_csv_transactions,
        name='db_records_csv_transactions'),
    re_path(r'^db_records_aqsa_backup/(?P<pk>\d+)$', vdrcb.db_records_aqsa_backup, name='db_records_aqsa_backup'),
]
# </CSV WITH WALLETS, CATEGORIES, TAGS, CONTACTS, TRANSACTIONS. BACKUP (ALL IN ONE ZIP)
