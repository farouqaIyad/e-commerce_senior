from catalog.serializers import ProductSerializer, Product
from rest_framework import serializers
from .models import ShoppingCart, Order, ShoppingCartProducts
from address.models import Address
from catalog.serializers import ProductDetailSerializer
from django.db import models

class ShoppingCartProductsSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)

    class Meta:
        model = ShoppingCartProducts
        fields = ["product", "quantity"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart = ShoppingCartProductsSerializer(many=True, read_only=True)

    # @staticmethod
    # def setup_eager_loading(queryset):
    #     return queryset.select_related('shopping_cart')

    class Meta:
        model = ShoppingCart
        fields = ["pk", "shopping_cart", "total_price"]
        read_only_fields = ["total_price"]


class OrderSerializer(serializers.ModelSerializer):
    shopping_cart = models.OneToOneField(ShoppingCart,on_delete=models.CASCADE)
    order_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    shopping_cart_serializer = ShoppingCartSerializer(read_only = True)

    def create(self, validated_data):
        validated_data["shopping_cart"] = self.context.get('shopping_cart')
        validated_data['order_address'] = self.context.get("order_address")
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = [
            "date_created",
            "date_deliverd",
            "order_status",
            "address",
            "total_cost",
            "shopping_cart_serializer"
        ]
        read_only_fields = ("date_created", "date_deliverd", "order_status")
