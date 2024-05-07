from .models import (
    Product,
    Category,
    ProductType,
    ProductDetail,
    ProductImage,
    ProductColor,
    ProductSize,
    ProductTypeSizes,
    Size_Value,
)
from user_feedback.serializers import ReviewSerializer
from rest_framework import serializers
from django.db.models import Avg
from deals.models import Deals
from Users.models import User
from django.db import models


class CategorySerializer(serializers.ModelSerializer):
    is_leaf = serializers.SerializerMethodField()

    def get_is_leaf(self, obj):
        is_leaf = obj.is_leaf_node()
        return is_leaf

    class Meta:
        model = Category
        fields = ["id", "name", "description", "parent", "is_leaf", "is_active"]
        read_only_fields = ["id", "is_leaf"]


class ProductTypeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["product_size"] = self.context.get("product_size")

        return super().create(validated_data)

    class Meta:
        model = ProductType
        fields = ["name", "product_size"]


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["size_type"]


class ProductSizeValueSerializer(serializers.ModelSerializer):
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["size"] = self.context.get("size")

        return super().create(validated_data)

    class Meta:
        model = Size_Value
        fields = ["value"]


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = ["color"]


class ProductRegisterSerializer(serializers.ModelSerializer):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE)
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
            "price",
            "description",
            "category",
            "product_type",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        average_rating = obj.review_set.aggregate(Avg("rating"))["rating__avg"]
        return average_rating if average_rating else 0

    def get_reviews_count(self, obj):
        reviews_count = obj.review_set.all().count()
        return reviews_count if reviews_count is not None else 0"""

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "price",
            "sale_price",
            # "average_rating",
            # "reviews_count",
            # "image",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    color = ProductColorSerializer(many=True, read_only=True)
    size = ProductSizeValueSerializer(read_only=True, many=True)

    class Meta:
        model = ProductDetail
        fields = "__all__"
