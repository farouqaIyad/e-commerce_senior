from django.db import models
from Users.models import User
from django.contrib.auth.models import BaseUserManager
from .utils import validate_lat, validate_long


class SupplierManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SUPPLIER)


class Supplier(User):
    base_role = User.Role.SUPPLIER
    supplier = SupplierManager()

    class Meta:
        proxy = True


class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    details = models.TextField(blank=True)
    phone_number = models.CharField(max_length=10)
    latitude = models.FloatField(default=0.00, validators=[validate_lat])
    longitude = models.FloatField(default=0.00, validators=[validate_long])
    commercial_recored = models.ImageField(
        upload_to="commercial_records", default="commercial_records/default.png"
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = "supplier"

    def __str__(self):
        return '{}'.format(self.user.username)
