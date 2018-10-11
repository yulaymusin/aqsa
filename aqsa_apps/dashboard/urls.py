# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views as v


dashboard_urlpatterns = [
    url(r'^$', v.home, name='home'),
]
