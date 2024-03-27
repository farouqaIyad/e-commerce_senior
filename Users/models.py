from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.utils import timezone

class User(AbstractBaseUser):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'User'
    
class Admin(models.Model):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)
    role_types = (('admin','admin'),('content_manager','content_manager'))
    Role = models.CharField(max_length = 30,choices = role_types)

    class Meta:
        db_table = 'Admin'



class Supplier(models.Model):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)
    website = models.URLField()
    #products = models.ManyToOneRel()

    class Meta:
        db_table = 'Supplier'
    

class Customer(models.Model):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)
    #shipping_address = models.ManyToOneRel()

    class Meta:
        db_table = 'Customer'


class Driver(models.Model):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)
    #address = models.CharField()

    class Meta:
        db_table = 'Driver'


class CustomerSupporter(models.Model):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=False,null=False)
    date_joined = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'CustomerSupporter'






 


