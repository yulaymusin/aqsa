# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from . import views as v

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', v.home, name='home'),
]
