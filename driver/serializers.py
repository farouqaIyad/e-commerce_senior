from .models import DriverProfile
from rest_framework import serializers
from Users.serializers import UserSerializer

class DriverProfileSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(required=True)
    user = UserSerializer(read_only = True)


    class Meta:
        model = DriverProfile
        fields = ["id", "user","is_approved", "latitude", "longitude", "phone_number","vehicle_type","vehicle_plate","vehicle_image"]
        read_only_fields = ["is_approved","user"]
