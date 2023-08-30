from django.db import models

# Create your models here.
class docdb(models.Model):
    """
    pmcid = models.CharField(default=None, max_length=25,unique=True, null= True, blank= True)
    pmid = models.CharField(default=None, max_length=25, null=True, blank=True)
    isValidId = models.BooleanField(default=False)
    title = models.CharField(default=None, max_length=10000, null=True, blank=True)
    abstract = models.TextField(default=None, null=True, blank=True)
    author = models.CharField(default=None, max_length=10000, null=True, blank=True)
    degree = models.IntegerField(default= None, null=True, blank=True)
    parents = models.CharField(default=None, max_length=10000, null=True, blank=True)
    children = models.CharField(default=None, max_length=10000, null=True, blank=True)
    numparents = models.IntegerField(default= None, null=True, blank=True)
    numchildren = models.IntegerField(default= None, null=True, blank=True)
    """
    pmcid = models.CharField(default=None, max_length=25, unique=True, null=True, blank=True)
    pmid = models.CharField(default=None, max_length=25, null=True, blank=True)
    isValidId = models.BooleanField(default=False)
    title = models.TextField(default=None, null=True, blank=True)
    abstract = models.TextField(default=None, null=True, blank=True)
    author = models.TextField(default=None, null=True, blank=True)
    degree = models.IntegerField(default=None, null=True, blank=True)
    parents = models.TextField(default=None,  null=True, blank=True)
    children = models.TextField(default=None, null=True, blank=True)
    numparents = models.IntegerField(default=None, null=True, blank=True)
    numchildren = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.pmcid
