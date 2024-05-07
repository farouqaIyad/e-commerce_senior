from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from catalog.models import Product
from django.utils import timezone
from Users.models import User
from django.db import models


class Deals(models.Model):
    name = models.CharField(max_length=255, unique=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99.99)],
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_ended = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "deals"


@receiver(post_save, sender=Deals)
def set_new_price(sender, instance, created, **kwargs):
    if created:
        products = instance.product.all()
        for product in products:
            product.new_price = (
                product.price - (product.price * instance.discount) / 100
            )
            product.save()


@receiver(post_delete, sender=Deals)
def delete_new_price(sender, instance, created, **kwargs):
    if created:
        products = instance.product.all()
        for product in products:
            product.new_price = product.price
            product.save()
