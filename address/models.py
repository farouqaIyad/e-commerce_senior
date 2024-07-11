from django.db import models
from Users.models import CustomerProfile
from .utils import validate_lat, validate_long


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
