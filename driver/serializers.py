from .models import DriverProfile
from rest_framework import serializers


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ["id", "is_approved", "latitude", "longitude", "phone_number"]
        read_only_fields = ["is_approved"]
