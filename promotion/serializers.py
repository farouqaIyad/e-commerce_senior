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
        fields = "__all__"
