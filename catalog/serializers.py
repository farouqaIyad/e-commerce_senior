from .models import (
    Category,
    ProductColor,
    ProductSize,
    Size_Value,
    ProductAttribute,
    Brand,
    CategoriesBrand,
    ProductCategoryAttributes,
)
from rest_framework import serializers
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
            "slug",
            "parent",
            "is_leaf",
            "is_active",
            "image_url",
        ]
        read_only_fields = ["id", "is_leaf", "slug"]


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["product_size"]


class ProductSizeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size_Value
        fields = ["id", "value"]
        read_only_fields = ["id"]


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = "__all__"


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ["name"]


class ProductCategoryAttributesSerializer(serializers.ModelSerializer):
    product_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["attribute"] = self.context.get("attribute")
        validated_data["product_type"] = self.context.get("product_type")
        return super().create(validated_data)

    class Meta:
        model = ProductCategoryAttributes
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]
