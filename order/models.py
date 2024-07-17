from .utils import validate_lat, validate_long
from wishlist_cart.models import ShoppingCart
from Users.models import CustomerProfile
from django.utils import timezone
from django.db import models
from promotion.models import UsedCoupons
from rest_framework.response import Response

class Address(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    details = models.TextField()
    phone_number = models.CharField(max_length=10)
    latitude = models.FloatField(default=0.00, validators=[validate_lat])
    longitude = models.FloatField(default=0.00, validators=[validate_long])

    class Meta:
        db_table = "address"
        unique_together = [["customer", "address_name"]]


class Order(models.Model):
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    used_coupon = models.ForeignKey(UsedCoupons,on_delete=models.CASCADE,null = True, blank = True)
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

    def save(self,*args,**kwargs):
        if self.used_coupon:
            max_uses = self.used_coupon.coupon_id.user_max_use
            times_used = self.used_coupon.times_used
            
            if max_uses<=times_used:
                return Response({"message":"can't use this coupon any more"})
            else:
                supplier = self.used_coupon.coupon_id.supplier
                supplier_products = self.shopping_cart.shopping_cart.filter(product__product__supplier = supplier)
                count = 0
                for product in supplier_products:
                    count += product.quantity
                if count+times_used >= max_uses:
                    return Response({"message":"exceeded coupon limit usage"})
                self.used_coupon.times_used+=count
                return super().save(*args)

