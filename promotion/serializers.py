from .models import Coupon, Promotion, ProductOnPromotion
from rest_framework import serializers
from django.db.models import Avg
from django.db import models


class CouponSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["supplier"] = self.context.get("supplier")
        return super().create(validated_data)

    class Meta:
        model = Coupon
        fields = ["name", "coupon_code", "discount_value", "user_max_use"]


class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = "__all__"


class ProductOnPromotionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["products"] = self.context.get("products")
        validated_data["promotion"] = self.context.get("promotion")
        return super().create(validated_data)

    class Meta:
        model = ProductOnPromotion
        fields = "__all__"
