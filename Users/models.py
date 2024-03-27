from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

class User(AbstractBaseUser):
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True,editable= False)
    first_name = models.CharField(max_length = 30,blank=True,null=True)
    last_name = models.CharField(max_length = 30,blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    password = models.CharField(max_length = 256,blank=True,null=True)
    date_joined = models.DateField(auto_now_add = True) 
    
    
class Admin(User):
    role_types = (('admin','admin'),('content_manager','content_manager'))
    Role = models.CharField(max_length = 30,choices = role_types)
    
class Supplier(User):
    
    #website = this one shall be a slug
    products = models.ManyToOneRel
    

class Customer(models.Model):
    pass

class Driver(models.Model):
    pass

class CustomerSupporter(models.Model):
    pass




 


