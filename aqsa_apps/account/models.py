from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    class Meta:
        db_table = 'account'
        ordering = ('pk',)

    user = models.OneToOneField(User, models.CASCADE)
    # TODO: time_zone = models.
    language = models.CharField(max_length=5, default='en', choices=settings.LANGUAGES, verbose_name=_('Language'))
