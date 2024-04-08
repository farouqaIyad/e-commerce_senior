from catalog.serializers import ProductSerializer,Product
from rest_framework import serializers
from .models import ShoppingCart, Order
from address.serializers import AddressSerializer

class ShoppingCartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_products(self,obj):
        products = obj.product.all()
        serializer = ProductSerializer(products, many = True)
        return serializer.data
    
    def get_total_cost(self,obj):
        products = obj.product.all()
        total_cost = 0
        for product in products:
            total_cost+=product.price
        return total_cost

    class Meta:
        model = ShoppingCart
        fields = ['products','total_cost']


class OrderSerializer(ShoppingCartSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self,obj):
        address = obj.order_address
        serializer = AddressSerializer(instance=address)
        return serializer.data
    
    class Meta:
        model = Order
        fields = ['products', 'date_created', 'date_deliverd', 'order_status','address','total_cost']
        read_only_fields = ('date_created', 'date_deliverd', 'order_status')