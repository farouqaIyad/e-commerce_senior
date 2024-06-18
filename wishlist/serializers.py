from catalog.serializers import ProductDetail
from rest_framework import serializers


class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("color", "size", "product")
        return queryset

    class Meta:
        model = ProductDetail
        fields = ["product", "id", "color", "size", "price", "sale_price"]
