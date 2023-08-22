from __future__ import unicode_literals

from django.db import models
class User(models.Model):
    username = models.CharField(max_length=255, default="NONE", primary_key=True)
    email = models.EmailField(default="NONE@NONE.com")
    name = models.CharField(max_length=2552, default="NONE")
    password = models.CharField(max_length=25, default="NONE")
    password2 = models.CharField(max_length=25, default="NONE")
    def __str__(self):
        return self.username


