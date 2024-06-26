from rest_framework import serializers
from .models import User, Address
from django.db import models


class AddressSerializer(serializers.ModelSerializer):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["customer"] = self.context.get("customer")
        return super().create(validated_data)

    class Meta:
        model = Address
        fields = [
            "address_name",
            "city",
            "district",
            "details",
            "phone_number",
        ]
