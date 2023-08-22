from __future__ import unicode_literals

from django.db import models
class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=25)
    def __str__(self):
        return self.username


