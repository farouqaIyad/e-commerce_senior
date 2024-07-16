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


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER
    customer = CustomerManager()

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


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    fcm_token = models.CharField(max_length=100,default = 'empty')

    def __str__(self):
        return "{}".format(self.user.get_full_name())


class CustomerSupportProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
