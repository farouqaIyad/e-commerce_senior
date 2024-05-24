from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.db import models
from .models import (
    User,
    SupplierProfile,
    CustomerProfile,
    DriverProfile,
    CustomerSupportProfile,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "username", "role"]
        read_only_fields = ["role"]


class SupplierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProfile
        fields = ["brand_name", "brand_location", "commercial_recored", "is_approved"]
        read_only_fields = ["is_approved"]


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ["id", "is_approved"]
        read_only_fields = ["is_approved"]


class CustomerSupportProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupportProfile
        fields = ["id", "user"]
