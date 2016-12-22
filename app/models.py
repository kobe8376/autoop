from django.db import models

# Create your models here.
class webuser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    privileges = models.IntegerField(max_length=2)
    createdate = models.DateTimeField(auto_now_add=True)
class sappinfo(models.Model):
    filename = models.CharField(max_length=50,null=False)
    version = models.CharField(max_length=50,null=False)
    createdate = models.DateField(auto_now_add=True,null=False)
    filepath = models.CharField(max_length=300,null=False)
class Tappinfo(models.Model):
    filename = models.CharField(max_length=50,null=False)
    version = models.CharField(max_length=50,null=False)
    createdate = models.DateField(auto_now_add=True,null=False)
    filepath = models.CharField(max_length=300,null=False)