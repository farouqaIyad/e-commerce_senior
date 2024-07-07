from catalog.serializers import UndetailedProductSerializer, Product
from rest_framework import serializers
from .models import ShoppingCart, Order, ShoppingCartProducts
from address.models import Address
from catalog.serializers import ProductDetail
from django.db import models


class ShoppingDetailSerializer(serializers.ModelSerializer):
    product = UndetailedProductSerializer(read_only=True)
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("color", "size", "product")
        return queryset

    class Meta:
        model = ProductDetail
        fields = ["product", "id", "color", "size", "price", "sale_price"]


class ShoppingCartProductsSerializer(serializers.ModelSerializer):
    product = ShoppingDetailSerializer(read_only=True)

    class Meta:
        model = ShoppingCartProducts
        fields = ["product", "quantity"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart = ShoppingCartProductsSerializer(read_only=True, many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.prefetch_related(
            "shopping_cart",
            "shopping_cart__product",
            "shopping_cart__product__color",
            "shopping_cart__product__size",
            "shopping_cart__product__product",
        )

    class Meta:
        model = ShoppingCart
        fields = ["pk", "shopping_cart", "total_price"]
        read_only_fields = ["total_price"]


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
