from .models import DriverProfile,vehicletypecategory
from rest_framework import serializers
from Users.serializers import UserSerializer
from django.contrib.sites.models import Site
from django.conf import settings


class DriverProfileSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(required=True, use_url=True)
    user = UserSerializer(read_only=True)
    # vehicle_image = serializers.SerializerMethodField()

    # def get_vehicle_image(self, obj):
    #     return "http://%s%s%s" % (
    #         Site.objects.get_current().domain,
    #         settings.MEDIA_URL,
    #         obj.vehicle_image,
    #     )

    class Meta:
        model = DriverProfile
        fields = [
            "id",
            "user",
            "is_approved",
            "latitude",
            "longitude",
            "phone_number",
            "vehicle_type",
            "vehicle_plate",
            "vehicle_image",
            "is_online",
        ]
        read_only_fields = ["is_approved", "user"]


