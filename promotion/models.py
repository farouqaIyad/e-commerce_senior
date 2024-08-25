from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from inventory.models import Product, ProductDetail
from Users.models import User, CustomerProfile
from supplier.models import SupplierProfile


class Coupon(models.Model):
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=10)
    supplier = models.OneToOneField(SupplierProfile, on_delete=models.CASCADE)
    discount_value = models.IntegerField()
    user_max_use = models.IntegerField(blank=True, null=True)
    products_to_earn = models.IntegerField(null=False, blank=False)
    time_start = models.DateField(default="2025-05-04")
    time_end = models.DateField(default="2025-05-05")
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "coupon"


class UsedCoupons(models.Model):
    coupon_id = models.ForeignKey(
        Coupon, related_name="used_coupons", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, related_name="customer_coupon"
    )
    times_used = models.IntegerField(default=0)

    class Meta:
        db_table = "usedcoupons"


class Promotion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    discount_percentege = models.IntegerField(blank=False, null=False)
    time_start = models.DateField()
    time_end = models.DateField()
    is_active = models.BooleanField(default=False)
    # celery well use this field
    is_scheduled = models.BooleanField(default=True)
    image_url = models.ImageField(
        unique=False, upload_to="promotions", default="promotions/default.png"
    )

    def clean(self):
        if self.time_start > self.time_end:
            raise ValidationError(_("end date before the start date"))

    class Meta:
        db_table = "promotion"


class ProductOnPromotion(models.Model):
    product = models.OneToOneField(
        Product, related_name="products_on_promotion", on_delete=models.CASCADE
    )
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_promotion"
