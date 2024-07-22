from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.db import models
from .models import (
    User,
    CustomerProfile,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


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
    user = UserSerializer(read_only=True, partial=True)
    image_url = serializers.ImageField(required=True, use_url=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("user")
        return queryset

    class Meta:
        model = CustomerProfile
        fields = ["id", "user", "phone_number", "image_url"]

    def update(self, instance, validated_data):
        user_data = {}
        user_data["email"] = self.context.get("email")
        user_data["first_name"] = self.context.get("first_name")
        user_data["last_name"] = self.context.get("last_name")
        User.objects.filter(customerprofile=instance).update(**user_data)
        instance.phone_number = validated_data.pop("phone_number")
        if "image_url" in validated_data:
            instance.image_url = validated_data.pop("image_url")
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad token")
