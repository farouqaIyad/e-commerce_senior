from django.db import models
from django.contrib.auth.models import BaseUserManager
from Users.models import User
from .utils import validate_lat, validate_long


class DriverManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DRIVER)


class Driver(User):
    base_role = User.Role.DRIVER
    driver = DriverManager()

    class Meta:
        proxy = True


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    latitude = models.FloatField(default=0.00, validators=[validate_lat])
    longitude = models.FloatField(default=0.00, validators=[validate_long])
    phone_number = models.CharField(max_length=15, unique=True)
