from rest_framework import serializers
from Users.serializers import UserSerializer
from .models import SupplierProfile, Supplier


class SupplierProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    commercial_recored = serializers.ImageField(required=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("user")
        return queryset

    class Meta:
        model = SupplierProfile
        fields = [
            "id",
            "user",
            "city",
            "district",
            "details",
            "phone_number",
            "latitude",
            "longitude",
            "commercial_recored",
            "is_approved",
        ]
        read_only_fields = ["is_approved", "user"]
