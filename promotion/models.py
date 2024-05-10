from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import ProductDetail
from Users.models import SupplierProfile


class Coupon(models.Model):
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=10)
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    discount_percentege = models.IntegerField()

    class Meta:
        db_table = "coupon"
        unique_together = ("coupon_code", "supplier")


class Promotion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    discount_percentege = models.IntegerField()
    time_start = models.DateField()
    time_end = models.DateField()
    is_active = models.BooleanField(default=False)
    # celery well use this field
    is_scheduled = models.BooleanField(default=False)

    def clean(self):
        if self.time_start > self.time_end:
            raise ValidationError(_("end date before the start date"))

    class Meta:
        db_table = "promotion"


class ProductOnPromotion(models.Model):
    product_detail_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    promotion_id = models.OneToOneField(Promotion, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_promotion"
