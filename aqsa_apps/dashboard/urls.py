# Author of Aqsa: Yulay Musin
from django.urls import re_path
from . import views as v

app_name = 'dashboard'

urlpatterns = [
    re_path(r'^$', v.home, name='home'),
]
