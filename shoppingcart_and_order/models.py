from django.db.models.signals import post_save
from Users.models import CustomerProfile
from catalog.models import ProductDetail
from django.dispatch import receiver
from address.models import Address
from django.utils import timezone
from django.db import models


class ShoppingCart(models.Model):
    customer = models.OneToOneField(
        CustomerProfile, on_delete=models.CASCADE, primary_key=True
    )
    products = models.ManyToManyField(
        ProductDetail, blank=True, through="ShoppingCartProducts"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        unique=False,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "shoppingcart"


class ShoppingCartProducts(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart, related_name="shopping_cart", on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "shoppingcartproducts"


@receiver(post_save, sender=CustomerProfile)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(customer=instance)


class Order(models.Model):
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_deliverd = models.DateTimeField(blank=True, null=True)
    order_status_type = (
        ("Preprocessing", "Preprocessing"),
        ("Awaiting Pickup", "Awaiting Pickup"),
        ("Picked up", "Picked up"),
        ("Deliverd", "Deliverd"),
        ("Cancelled", "Cancelled"),
    )
    order_status = models.CharField(
        max_length=30, choices=order_status_type, default="Preprocessing"
    )
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        unique=False,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "order"

