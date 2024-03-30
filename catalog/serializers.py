from rest_framework import serializers
from .models import Product,Category,SubCategory
from django.db import models
from Users.models import User

class CategorySerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        return super().create(validated_data)
    class Meta:
        model = Category
        fields = ['name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name','category']


class ProductSerializer(serializers.ModelSerializer):
    supplier = models.ForeignKey(User,on_delete = models.CASCADE)

    def create(self,validated_data):
        request = self.context.get('request')
        if request is not None:
            supplier_id =request.user.id
            validated_data['supplier'] = supplier_id
            return super().create(validated_data)
        else:
            return serializers.ValidationError()
        
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category','sub_category','quantity_in_stock']
