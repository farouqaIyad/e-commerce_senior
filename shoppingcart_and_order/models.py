from django.db import models
from Users.models import User
# Create your models here.

class ShoppingCart(models.Model):
    customer = models.ForeignKey(User,on_delete = models.CASCADE)
    cart_name = models.CharField(max_length=30, blank=True)


    class Meta:
        db_table = 'shoppingcart'

