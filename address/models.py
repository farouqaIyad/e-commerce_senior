from django.db import models
from Users.models import User


class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    details = models.TextField()
    phone_number = models.IntegerField()

    class Meta:
        db_table = "address"
        unique_together = [["customer", "address_name"]]
