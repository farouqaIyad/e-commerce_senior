from django.db import models
from django.contrib.auth.models import BaseUserManager
from Users.models import User
from .utils import validate_lat, validate_long
from catalog.models import Category

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
    vehicle_types = (
        ("BIKE", "Bike"),
        ("CAR", "Car"),
        ("TRUCK", "Truck"),
    )

    vehicle_type = models.CharField(max_length=9, choices=vehicle_types, blank=False)
    vehicle_plate = models.CharField(max_length=10, blank=False, unique=True)
    vehicle_image = models.ImageField(upload_to="driver", default="drivers/default")
    is_online = models.BooleanField(default=True)


class vehicletypecategory(models.Model):
    vehicle_types = (
        ("BIKE", "Bike"),
        ("CAR", "Car"),
        ("TRUCK", "Truck"),
    )

    vehicle_type = models.CharField(max_length=9, choices=vehicle_types, blank=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'vehicletypecategory'