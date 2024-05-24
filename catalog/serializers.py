from .models import (
    Product,
    Category,
    ProductType,
    ProductDetail,
    ProductColor,
    ProductSize,
    Size_Value,
)
from user_feedback.serializers import ReviewSerializer
from rest_framework import serializers
from django.db.models import Avg
from Users.models import SupplierProfile
from django.db import models


class CategorySerializer(serializers.ModelSerializer):
    is_leaf = serializers.SerializerMethodField()

    def get_is_leaf(self, obj):
        is_leaf = obj.is_leaf_node()
        return is_leaf

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "parent",
            "is_leaf",
            "is_active",
            "category_image",
        ]
        read_only_fields = ["id", "is_leaf"]


class ProductTypeSerializer(serializers.ModelSerializer):
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["product_size"] = self.context.get("product_size")
        validated_data["category"] = self.context.get("category")

        return super().create(validated_data)

    class Meta:
        model = ProductType
        fields = ["name", "product_size", "category"]
        depth = 1


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["product_size"]


class ProductSizeValueSerializer(serializers.ModelSerializer):
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["size"] = self.context.get("size")

        return super().create(validated_data)

    class Meta:
        model = Size_Value
        fields = ["id", "value", "size"]
        read_only_fields = ["id"]


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = "__all__"


class ProductRegisterSerializer(serializers.ModelSerializer):
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["supplier"] = self.context.get("supplier")
        validated_data["category"] = self.context.get("category")
        validated_data["product_type"] = self.context.get("product_type")
        return super().create(validated_data)

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "product_type",
        ]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "main_price",
            "main_sale_price",
            "average_rating",
            "reviews_count",
            "main_image",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    color = ProductColorSerializer(many=True, read_only=True)
    size = ProductSizeValueSerializer(read_only=True, many=True)

    class Meta:
        model = ProductDetail
        fields = [
            "id",
            "color",
            "size",
            "sku",
            "price",
            "sale_price",
            "is_active",
            "is_main",
            "product",
        ]
        depth = 1


class ProductPageSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"
