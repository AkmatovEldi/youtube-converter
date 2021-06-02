from django.contrib.auth.models import User
from django.db import models


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
