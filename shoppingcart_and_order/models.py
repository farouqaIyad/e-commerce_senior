from Users.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from catalog.models import Product
from django.utils import timezone

class ShoppingCart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    product = models.ManyToManyField(Product, blank=True)

    class Meta:
        db_table = 'shoppingcart'

@receiver(post_save, sender=User)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:  
        ShoppingCart.objects.create(customer = instance)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    date_created = models.DateTimeField(default=timezone.now)
    date_deliverd = models.DateTimeField(blank=True,null = True)
    order_status_type = (('Preprocessing', 'Preprocessing'), ('Awaiting Pickup', 'Awaiting Pickup'),
                         ('Picked up', 'Picked up'), ('Deliverd', 'Deliverd'), ('Cancelled', 'Cancelled'))
    order_status = models.CharField(max_length=30, choices=order_status_type)

    class Meta:
        db_table = 'order'

@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:  
        products = instance.product.all()
        for product in products:
            product.quantity_in_stock-=1
            product.save()

