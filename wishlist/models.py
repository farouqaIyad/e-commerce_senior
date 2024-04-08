from django.utils import timezone
from django.db import models
from Users.models import User


class Wishlist(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    product = models.ManyToManyField(Product, blank=True)

    
    class Meta: 
        db_table = 'wishlist' 

@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:  
        Wishlist.objects.create(customer = instance)
    
    
    

