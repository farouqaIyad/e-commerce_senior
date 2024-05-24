from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import Product, ProductDetail
from Users.models import User, CustomerProfile, SupplierProfile


class Coupon(models.Model):
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=10)
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    discount_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        unique=True,
        null=True,
        blank=True,
    )
    user_max_use = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "coupon"


class UsedCoupons(models.Model):
    coupon_id = models.ForeignKey(
        Coupon, related_name="used_coupons", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    used_coupons = models.IntegerField()

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

