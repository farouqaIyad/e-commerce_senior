from user_feedback.serializers import ReviewSerializer
from .models import Product,Category,SubCategory
from rest_framework import serializers
from django.db.models import Avg
from Users.models import User
from django.db import models


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['category_name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    def create(self, validated_data):
        validated_data['category'] = self.context.get('category')
        return super().create(validated_data)
    
    class Meta:
        model = SubCategory
        fields = ['sub_category_name']

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    def get_average_rating(self,obj):
        average_rating = obj.review_set.aggregate(Avg('rating'))['rating__avg']
        return average_rating if average_rating else 0
    
    def get_reviews_count(self,obj):
        reviews_count = obj.review_set.all().count()
        return reviews_count if reviews_count is not None else 0

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'average_rating', 'reviews_count']

class ProductDetailSerializer(ProductSerializer):
    supplier = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)  
    reviews = serializers.SerializerMethodField()
    
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data

    def create(self,validated_data):
        validated_data['category'] = self.context.get('category')
        validated_data['supplier'] = self.context.get('supplier')
        product = super().create(validated_data)

        sub_category_data = validated_data.pop('sub_category', [])
        for sub_category_id in sub_category_data:
            sub_category, created = SubCategory.objects.get_or_create(pk = sub_category_id)
            product.sub_category.add(sub_category)
        return product
        
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'quantity_in_stock', 'category', 'sub_category', 'reviews', 'average_rating','reviews_count']


