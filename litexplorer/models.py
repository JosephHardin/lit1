from django.db import models

# Create your models here.
class iddb(models.Model):
    pmcid = models.CharField(default=None, max_length=25, primary_key=True)
    isValidId = models.BooleanField(default=False)
    degree = models.IntegerField(default=255, null=True, blank=True)
    def __str__(self):
        return self.pmcid

class docdb(models.Model):
    """
    pmcid = models.CharField(default=None, max_length=25,unique=True, null= True, blank= True)

    isValidId = models.BooleanField(default=False)
    title = models.CharField(default=None, max_length=10000, null=True, blank=True)
    abstract = models.TextField(default=None, null=True, blank=True)
    author = models.CharField(default=None, max_length=10000, null=True, blank=True)
    degree = models.IntegerField(default= None, null=True, blank=True)

    """
    pmcid = models.OneToOneField(iddb, on_delete=models.CASCADE, primary_key=True)
    title = models.TextField(default=None, null=True, blank=True)
    abstract = models.TextField(default=None, null=True, blank=True)
    author = models.TextField(default=None, null=True, blank=True)



    def __str__(self):
        return self.pmcid
class citedb(models.Model):
    parent = models.ForeignKey(iddb, on_delete=models.CASCADE, related_name="parent")
    child = models.ForeignKey(iddb, on_delete=models.CASCADE, related_name="child")
