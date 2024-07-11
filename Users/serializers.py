from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.db import models
from .models import (
    User,
    CustomerProfile,
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
        fields = ["email", "password", "first_name", "last_name", "username"]
        read_only_fields = ["role"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("user")
        return queryset

    class Meta:
        model = CustomerProfile
        fields = ["id", "user", "phone_number"]
