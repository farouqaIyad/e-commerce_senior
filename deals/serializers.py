from catalog.serializers import ProductSerializer, Product
from rest_framework import serializers
from .models import Deals


class DealsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = obj.product.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def create(self, validated_data):
        validated_data["supplier"] = self.context.get("supplier")
        deal = super().create(validated_data)
        products = self.context.pop("products", [])
        for product in products:
            product = Product.objects.get(pk=product)
            deal.product.add(product)
        return deal

    class Meta:
        model = Deals
        fields = ["name", "products", "discount", "date_ended"]
