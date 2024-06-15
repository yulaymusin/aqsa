# Author of Aqsa: Yulay Musin
from django.urls import re_path
from django.views.generic import TemplateView

app_name = 'about'

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='about/homepage.html'), name='homepage'),
    # TODO make instruction for users
    # re_path(r'how_to_use^$', TemplateView.as_view(template_name='about/how_to_use.html'), name='how_to_use'),
]
