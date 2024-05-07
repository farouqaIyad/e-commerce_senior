from catalog.serializers import ProductSerializer, Product
from rest_framework import serializers
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = obj.product.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    class Meta:
        model = Wishlist
        fields = ["products"]
