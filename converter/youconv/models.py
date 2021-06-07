from django.contrib.auth.models import User
from django.db import models


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    file_name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return '"%s": %s' % (self.file_name, self.user)
