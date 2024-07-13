from wishlist_cart.serializers import ShoppingCartSerializer
from rest_framework import serializers
from django.db import models
from .models import Order, Address, CustomerProfile


class AddressSerializer(serializers.ModelSerializer):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

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
            "latitude",
            "longitude",
            "phone_number",
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shopping_cart = ShoppingCartSerializer(read_only=True)

    def create(self, validated_data):
        validated_data["shopping_cart"] = self.context.get("shopping_cart")
        validated_data["order_address"] = self.context.get("order_address")
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = [
            "date_created",
            "date_deliverd",
            "order_status",
            "order_address",
            "total_cost",
            "shopping_cart",
        ]
        read_only_fields = ("date_created", "date_deliverd", "order_status")
        depth = 1
