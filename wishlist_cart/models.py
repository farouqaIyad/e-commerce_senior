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


class ShoppingCart(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
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

    def __str__(self, *args, **kwargs):
        return "{}".format(self.total_price)


class ShoppingCartProducts(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart, related_name="shopping_cart", on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "shoppingcartproducts"
