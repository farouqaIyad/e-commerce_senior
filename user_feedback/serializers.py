from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Review, Returnal, ReturnMethod, ReturnReason
from inventory.models import Product
from Users.models import User
from django.db import models


class ReviewSerializer(serializers.ModelSerializer):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = serializers.StringRelatedField()

    def create(self, validated_data):
        product = self.context.get("product")
        customer = self.context.get("customer")
        validated_data["product"] = product
        validated_data["customer"] = customer
        if Review.objects.filter(customer=customer, product=product).exists():
            raise ValidationError("User has already reviewed this product.")

        return super().create(validated_data)

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "customer"]
        read_only_fields = ("customer",)


class ReturnReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnReason
        fields = ["id", "value"]


class ReturnMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnMethod
        fields = ["id", "return_method", "fees_applied"]


class ReturnalSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product_detail = self.context.get("product_detail")
        customer = self.context.get("customer")
        return_reason = self.context.get("return_reason")
        return_method = self.context.get("return_method")
        validated_data["customer"] = customer
        validated_data["product_detail"] = product_detail
        validated_data["return_reason"] = return_reason
        validated_data["return_method"] = return_method

        return super().create(validated_data)

    class Meta:
        model = Returnal
        fields = [
            "id",
            "customer",
            "product_detail",
            "return_reason",
            "return_method",
            "comment",
            "date_created",
            "image",
        ]
