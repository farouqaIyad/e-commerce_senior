from rest_framework import serializers
from catalog.serializers import UndetailedProductSerializer, ProductDetail
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
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
