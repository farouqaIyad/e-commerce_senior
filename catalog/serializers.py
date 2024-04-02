from rest_framework import serializers
from .models import Product,Category,SubCategory
from django.db import models
from Users.models import User
from user_feedback.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['category_name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = models.ForeignKey(Category,on_delete =models.CASCADE)
    
    def create(self,validated_data):
        validated_data['category'] = self.context.get('category')
        return super().create(validated_data)
    
    class Meta:
        model = SubCategory
        fields = ['sub_category_name','category']


class ProductSerializer(serializers.ModelSerializer):
    supplier = models.ForeignKey(User,on_delete = models.CASCADE)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    reviews = serializers.SerializerMethodField()
    
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews,many = True)
        return serializer.data

    def create(self,validated_data):
        validated_data['category'] = self.context.get('category')
        validated_data['supplier'] = self.context.get('supplier')
        return super().create(validated_data)
        
    class Meta:
        model = Product
        fields = ['product_name','price','description','quantity_in_stock','category','sub_category','reviews']


class ProductsSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Product
        fields = ['product_name','price']
