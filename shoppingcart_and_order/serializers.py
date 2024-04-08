from catalog.serializers import ProductSerializer
from rest_framework import serializers
from catalog.models import Product
from .models import ShoppingCart, Order
from Users.models import User
from django.db import models


class ShoppingCartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_products(self,obj):
        products = obj.product.all()
        serializer = ProductSerializer(products, many = True)
        return serializer.data
    
    def get_total_cost(self,obj):
        prices = obj.product.all()
        return prices

    class Meta:
        model = ShoppingCart
        fields = ['products','total_cost']


class OrderSerializer(ShoppingCartSerializer):
    
    class Meta:
        model = Order
        fields = ['products', 'date_created', 'date_deliverd', 'order_status']
        read_only_fields = ('date_created', 'date_deliverd', 'order_status')





