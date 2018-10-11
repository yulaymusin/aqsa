# Author of Aqsa: Yulay Musin
from django.conf.urls import url
from django.views.generic import TemplateView


about_urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='about/homepage.html'), name='homepage'),
    # TODO make instruction for users
    # url(r'how_to_use^$', TemplateView.as_view(template_name='about/how_to_use.html'), name='how_to_use'),
]
