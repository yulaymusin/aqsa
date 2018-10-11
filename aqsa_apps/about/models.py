# Author of Aqsa: Yulay Musin
from django.db import models


class ReasonToDeleteAccount(models.Model):
    class Meta:
        db_table = 'reason_to_delete'

    date = models.DateField(auto_now=True)
    reason = models.TextField()

    def __str__(self):
        return self.reason
