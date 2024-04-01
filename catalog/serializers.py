from rest_framework import serializers
from .models import Product,Category,SubCategory
from django.db import models
from Users.models import User

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name','category']


class ProductSerializer(serializers.ModelSerializer):
    supplier = models.ForeignKey(User,on_delete = models.CASCADE)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    
    def create(self,validated_data):
        validated_data['category'] = self.context.get('category')
        validated_data['supplier'] = self.context.get('supplier')
        return super().create(validated_data)
        
    class Meta:
        model = Product
        fields = ['name','price','description','quantity_in_stock','category','sub_category']
