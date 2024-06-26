from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPPLIER = "SUPPLIER", "Supplier"
        CUSTOMER = "CUSTOMER", "Customer"
        DRIVER = "DRIVER", "Driver"
        CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT", "Customer_support"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)
    base_role = Role.ADMIN

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class SupplierManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SUPPLIER)


class Supplier(User):
    base_role = User.Role.SUPPLIER
    supplier = SupplierManager()

    class Meta:
        proxy = True


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER
    customer = CustomerManager()

    class Meta:
        proxy = True


class DriverManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DRIVER)


class Driver(User):
    base_role = User.Role.DRIVER
    driver = DriverManager()

    class Meta:
        proxy = True


class CustomerSupportManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER_SUPPORT)


class CustomerSupport(User):
    base_role = User.Role.CUSTOMER_SUPPORT
    customer_support = CustomerSupportManager()

    class Meta:
        proxy = True


class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255, blank=False, null=False)
    brand_location = models.CharField(max_length=255)
    commercial_recored = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = "supplier"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)


class CustomerSupportProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
