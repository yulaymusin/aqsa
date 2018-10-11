# Author of Aqsa: Yulay Musin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include

from aqsa_apps.account.urls import before_login_urlpatterns, after_login_urlpatterns
from aqsa_apps.wallet_tag_etc.urls import wallet_tag_etc_urlpatterns
from aqsa_apps.transaction.urls import transaction_urlpatterns
from aqsa_apps.export_to_file.urls import export_to_file_urlpatterns
from aqsa_apps.import_from_file.urls import import_from_file_urlpatterns
from aqsa_apps.dashboard.urls import dashboard_urlpatterns
from aqsa_apps.report.urls import report_urlpatterns

from aqsa_apps.about.urls import about_urlpatterns

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = i18n_patterns(
    url(r'^registration/', include(before_login_urlpatterns)),
    url(r'^account/', include(after_login_urlpatterns, namespace='account')),
    url(r'^wallet_tag_etc/', include(wallet_tag_etc_urlpatterns, namespace='wallet_tag_etc')),
    url(r'^transaction/', include(transaction_urlpatterns, namespace='transaction')),
    url(r'^export_to_file/', include(export_to_file_urlpatterns, namespace='export_to_file')),
    url(r'^import_from_file/', include(import_from_file_urlpatterns, namespace='import_from_file')),
    url(r'^dashboard/', include(dashboard_urlpatterns, namespace='dashboard')),
    url(r'^report/', include(report_urlpatterns, namespace='report')),

    url(r'^', include(about_urlpatterns, namespace='about')),
)

urlpatterns += [
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
