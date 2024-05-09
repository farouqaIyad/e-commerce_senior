from django.utils import timezone
from django.db import models
from Users.models import CustomerProfile
from catalog.models import ProductDetail
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wishlist(models.Model):
    customer = models.OneToOneField(
        CustomerProfile, on_delete=models.CASCADE, primary_key=True
    )
    product = models.ManyToManyField(ProductDetail, blank=True)

    class Meta:
        db_table = "wishlist"


@receiver(post_save, sender=CustomerProfile)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(customer=instance)
