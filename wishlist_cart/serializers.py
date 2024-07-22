from rest_framework import serializers
from catalog.serializers import UndetailedProductSerializer, ProductDetail
from .models import ShoppingCart, ShoppingCartProducts


class WishlistSerializer(serializers.ModelSerializer):
    product = UndetailedProductSerializer(read_only=True)
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("color", "size", "product")
        return queryset

    class Meta:
        model = ProductDetail
        fields = ["product", "id", "color", "size", "price", "sale_price"]


class DetailedSerializer(serializers.ModelSerializer):
    product = UndetailedProductSerializer(read_only=True)
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()
    stock = serializers.StringRelatedField()

    class Meta:
        model = ProductDetail
        fields = ["product", "id", "color", "size", "price", "sale_price", "stock"]


class ShoppingCartProductsSerializer(serializers.ModelSerializer):
    product = DetailedSerializer(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            "product",
            "product__size",
            "product__color",
            "product__product",
            "product__stock",
        )
        return queryset

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
