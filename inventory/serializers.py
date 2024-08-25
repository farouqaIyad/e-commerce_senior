from rest_framework import serializers
from django.db import models
from supplier.models import SupplierProfile
from .models import (
    ProductImage,
    Product,
    ProductColor,
    Size_Value,
    ProductDetail,
    Stock,
    ProductAttributeValues,
    ProductImageSet,
    ImagesMaterializedView,
    ProductAttrsMaterializedViews
)
from catalog.serializers import ProductAttributeSerializer
from user_feedback.serializers import ReviewSerializer
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models import Prefetch


class ProductRegisterSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)

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


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ["image_url"]


class ProductImageSetSerializer(serializers.ModelSerializer):
    productimage_set = ProductImageSerializer(many=True)

    class Meta:
        model = ProductImageSet
        fields = ["productimage_set"]


class ProductDetailSerializer(serializers.ModelSerializer):
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()

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
            "image_set_id",
        ]


class ProductAttributesvaluesSerializer(serializers.ModelSerializer):
    # product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # def create(self, validated_data):
    #     validated_data["product_attr"] = self.context.get("product_attr")
    #     validated_data["product"] = self.context.get("product")
    #     return super().create(validated_data)
    product_attr = ProductAttributeSerializer()

    class Meta:
        model = ProductAttributeValues
        fields = ["value", "product_attr"]


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(many = True)
    review_set = ReviewSerializer(read_only=True, many=True)
    # in_wishlist = serializers.BooleanField(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            "review_set",
            "product_detail",
            "product_detail__color",
            "product_detail__size",
            
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
            "review_set"
            # # "in_wishlist",
        ]


class UndetailedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "average_rating",
            "reviews_count",
            "main_image",
            "supplier",
        ]


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "main_image",
        ]


class StockSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True)

    def update(self, instance, validated_data):

        product_data = {}
        if "color" in self.context:
            if self.context.get("color"):
                product_data["color"] = self.context.get("color")
        if "size" in self.context:
            if self.context.get("size"):
                product_data["size"] = self.context.get("size")
        if "price" in self.context:
            if self.context.get("price"):
                product_data["price"] = self.context.get("price")
        if "is_active" in self.context:
            if not self.context.get("is_active"):
                product_data["is_active"] = self.context.get("is_active")
        if product_data:
            ProductDetail.objects.filter(stock=instance).update(**product_data)

        if "quantity_in_stock" in validated_data:
            if validated_data.pop("quantity_in_stock"):
                instance.quantity_in_stock = validated_data.pop("quantity_in_stock")
            instance.save()
        return instance

    class Meta:
        model = Stock
        fields = ["id", "product_detail", "quantity_in_stock", "products_sold"]
        read_only_fields = ["id", "product_detail", "products_sold"]


class ImagesMaterializedViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesMaterializedView
        fields = ["image_set", "image_url"]


class ProductAttrsMaterializedViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttrsMaterializedViews
        fields = "__all__"