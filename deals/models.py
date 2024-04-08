from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from catalog.models import Product
from django.utils import timezone
from Users.models import User
from django.db import models 


class Deals(models.Model):
    name = models.CharField(max_length = 255, unique=True) 
    supplier = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ManyToManyField(Product)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_created = models.DateTimeField(default = timezone.now)
    date_ended = models.DateTimeField(blank = True, null = True)