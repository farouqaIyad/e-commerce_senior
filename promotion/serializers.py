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
        fields = [
            "supplier",
            "id",
            "name",
            "coupon_code",
            "discount_value",
            "user_max_use",
            "products_to_earn",
            "time_start",
            "time_end",
            "is_active",
        ]
        write_only_fields = ["coupon_code"]


class PromotionSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=True, use_url=True)

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
        execule = ["description"]
