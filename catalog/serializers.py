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
    Stock,
    Brand,
)
from django.conf import settings

from user_feedback.serializers import ReviewSerializer
from rest_framework import serializers
from django.db.models import Avg
from django.db import models
from supplier.models import SupplierProfile
from django.contrib.sites.models import Site


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


class ProductTypeSerializer(serializers.ModelSerializer):
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["product_size"] = self.context.get("product_size")
        validated_data["category"] = self.context.get("category")

        return super().create(validated_data)

    class Meta:
        model = ProductType
        fields = ["name", "product_size"]
        depth = 1


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


class ProductRegisterSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000, allow_empty_file=False, use_url=False
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
        boolean = True
        for image in uploaded_images:
            ProductImage.objects.create(
                image_url=image, product=product, is_main=boolean
            )
            boolean = False
        return product

    class Meta:
        model = Product
        fields = ["name", "description", "category", "product_type", "uploaded_images"]


class ProductSerializer(serializers.ModelSerializer):
    in_wishlist = serializers.BooleanField(read_only=True)

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
            "in_wishlist",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)

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
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return "http://%s%s%s" % (
            Site.objects.get_current().domain,
            settings.MEDIA_URL,
            obj.image_url,
        )

    class Meta:
        model = ProductImage
        fields = ["image_url"]


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True, many=True)
    review_set = ReviewSerializer(read_only=True, many=True)
    images = ProductImageSerializer(read_only=True, many=True)
    in_wishlist = serializers.BooleanField(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            "review_set",
            "product_detail",
            "product_detail__color",
            "product_detail__size",
            "images",
        )
        return queryset

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "main_price",
            "main_sale_price",
            "average_rating",
            "reviews_count",
            "main_image",
            "product_detail",
            "review_set",
            "images",
            "in_wishlist",
        ]


class StockSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "product_detail", "quantity_in_stock", "products_sold"]
        read_only_fields = ["id", "product_detail", "products_sold"]


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ["id", "name"]


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


class UndetailedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "average_rating",
            "reviews_count",
            "main_image",
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]
