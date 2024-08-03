from .utils import validate_lat, validate_long
from wishlist_cart.models import ShoppingCart, ProductDetail
from Users.models import CustomerProfile
from django.utils import timezone
from django.db import models
from promotion.models import UsedCoupons
from rest_framework.response import Response
from supplier.models import SupplierProfile
from driver.models import DriverProfile

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

    def __str__(self):
        return '{}'.format(self.details)


class Order(models.Model):
    cart = models.ForeignKey(
        ShoppingCart, related_name="cart", on_delete=models.CASCADE
    )
    used_coupon = models.ForeignKey(
        UsedCoupons, on_delete=models.CASCADE, null=True, blank=True
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_deliverd = models.DateTimeField(blank=True, null=True)
    order_status_type = (
        ("Preprocessing", "Preprocessing"),
        ("Picked up", "Picked up"),
        ("Deliverd", "Deliverd"),
        ("Cancelled", "Cancelled"),
    )
    order_status = models.CharField(
        max_length=30, choices=order_status_type, default="Preprocessing"
    )
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False, blank=False)
    products = models.ManyToManyField(
        ProductDetail, blank=True, through="OrderProducts"
    )
    vehicle_types = (
        ("BIKE", "Bike"),
        ("CAR", "Car"),
        ("TRUCK", "Truck"),
    )
    pick_up_method = models.CharField(max_length=9, choices=vehicle_types, blank=False)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,null=True,blank=True)
    delivery_image = models.ImageField(upload_to="orders", default="orders/default.png")

    
    class Meta:
        db_table = "order"

    def save(self, *args, **kwargs):
        if self.used_coupon:
            max_uses = self.used_coupon.coupon_id.user_max_use
            times_used = self.used_coupon.times_used

            if max_uses <= times_used:
                return Response({"message": "can't use this coupon any more"})
            else:
                supplier = self.used_coupon.coupon_id.supplier
                supplier_products = self.shopping_cart.shopping_cart.filter(
                    product__product__supplier=supplier
                )
                count = 0
                for product in supplier_products:
                    count += product.quantity
                if count + times_used >= max_uses:
                    return Response({"message": "exceeded coupon limit usage"})
                self.used_coupon.times_used += count
        return super().save(*args)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    products = models.ForeignKey(
        ProductDetail, related_name="cart_product_detail", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "order_products"


class ProductBoughtFromSupplier(models.Model):
    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, related_name="cus"
    )
    supplier = models.ForeignKey(
        SupplierProfile, on_delete=models.CASCADE, related_name="sup"
    )
    products_bought = models.IntegerField(default=0)

    class Meta:
        db_table = "productboughtfromsupplier"
