from .models import (
    Product,
    Category,
    ProductType,
    ProductDetail,
    ProductColor,
    ProductSize,
    Size_Value,
    ProductImage,
    ProductAttribute,
    ProductAttributeValues,
    ProductTypeAttributes,
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
            "slug",
            "parent",
            "is_leaf",
            "is_active",
            "image_url",
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
        depth = 1


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ["id", "image_url"]


class ProductRegisterSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=6, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["supplier"] = self.context.get("supplier")
        validated_data["category"] = self.context.get("category")
        validated_data["product_type"] = self.context.get("product_type")
        uploaded_images = validated_data.pop("uploaded_images")
        product = super().create(validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(image, product)
        return product

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
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ['id','name']


class ProductTypeAttributesSerializer(serializers.ModelSerializer):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["attribute"] = self.context.get("attribute")
        validated_data["product_type"] = self.context.get("product_type")
        return super().create(validated_data)

    class Meta:
        model = ProductTypeAttributes
        fields = "__all__"


class ProductAttributesvaluesSerializer(serializers.ModelSerializer):
    product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["product_attr"] = self.context.get("product_attr")
        validated_data["product"] = self.context.get("product")
        return super().create(validated_data)

    class Meta:
        model = ProductAttributeValues
        fields = "__all__"
