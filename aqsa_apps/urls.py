# Author of Aqsa: Yulay Musin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, re_path

from aqsa_apps.account.urls import before_login_urlpatterns

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = i18n_patterns(
    re_path(r'^registration/', include(before_login_urlpatterns)),
    re_path(r'^account/', include('aqsa_apps.account.urls')),
    re_path(r'^wallet_tag_etc/', include('aqsa_apps.wallet_tag_etc.urls')),
    re_path(r'^transaction/', include('aqsa_apps.transaction.urls')),
    re_path(r'^export_to_file/', include('aqsa_apps.export_to_file.urls')),
    re_path(r'^import_from_file/', include('aqsa_apps.import_from_file.urls')),
    re_path(r'^dashboard/', include('aqsa_apps.dashboard.urls')),
    re_path(r'^report/', include('aqsa_apps.report.urls')),

    re_path(r'^', include('aqsa_apps.about.urls')),
)

urlpatterns += [
    re_path(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    re_path(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
