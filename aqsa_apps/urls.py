# Author of Aqsa: Yulay Musin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include

from aqsa_apps.account.urls import before_login_urlpatterns

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = i18n_patterns(
    url(r'^registration/', include(before_login_urlpatterns)),
    url(r'^account/', include('aqsa_apps.account.urls')),
    url(r'^wallet_tag_etc/', include('aqsa_apps.wallet_tag_etc.urls')),
    url(r'^transaction/', include('aqsa_apps.transaction.urls')),
    url(r'^export_to_file/', include('aqsa_apps.export_to_file.urls')),
    url(r'^import_from_file/', include('aqsa_apps.import_from_file.urls')),
    url(r'^dashboard/', include('aqsa_apps.dashboard.urls')),
    url(r'^report/', include('aqsa_apps.report.urls')),

    url(r'^', include('aqsa_apps.about.urls')),
)

urlpatterns += [
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
