from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Review, Complaints
from catalog.models import Product
from Users.models import User
from django.db import models


class ReviewSerializer(serializers.ModelSerializer):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

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
        fields = ["rating", "comment", "customer"]
        read_only_fields = ("customer",)


class ComplaintsSerializer(serializers.ModelSerializer):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order,on_delete = models.CASCADE)

    def create(self, validated_data):
        validated_data["customer"] = self.context.get("customer")
        validated_data["order"] = self.context.get("order")

        return super().create(validated_data)

    class Meta:
        model = Complaints
        fields = ["order", "complain_type", "status_type"]
