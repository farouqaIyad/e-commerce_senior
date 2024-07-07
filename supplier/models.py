from django.db import models
from Users.models import User
from django.contrib.auth.models import BaseUserManager


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
    brand_name = models.CharField(max_length=255, blank=False, null=False)
    brand_location = models.CharField(max_length=255)
    commercial_recored = models.ImageField(
        upload_to="commercial_records", default="commercial_records/default.png"
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = "supplier"
