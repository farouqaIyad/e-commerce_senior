from .models import Order, Address, CustomerProfile, OrderProducts, ShoppingCart
from wishlist_cart.serializers import WishlistSerializer
from supplier.serializers import SupplierProfile,OrderSupplierSerializer
from rest_framework import serializers
from catalog.models import Product
from django.db import models
from .distance_alg import calculate_shortest_distance

class AddressSerializer(serializers.ModelSerializer):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    def create(self, validated_data):
        validated_data["customer"] = self.context.get("customer")
        return super().create(validated_data)

    class Meta:
        model = Address
        fields = [
            "id",
            "address_name",
            "city",
            "district",
            "details",
            "latitude",
            "longitude",
            "phone_number",
        ]


class OrderSerializer(serializers.ModelSerializer):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        products = Product.objects.filter(
            product_detail__cart_product_detail__order=obj
        ).values_list("main_image", flat=True)[:3]
        return products

    def create(self, validated_data):
        shopping_cart = self.context.get("cart")
        validated_data["order_address"] = self.context.get("order_address")
        validated_data["cart"] = shopping_cart
        order = Order.objects.create(**validated_data)
        products_data = {}
        products_data["order"] = order
        products = shopping_cart.shopping_cart.all()
        for product in products:
            products_data["products"] = product.product
            products_data["quantity"] = product.quantity
            OrderProducts.objects.create(**products_data)
        return order

    class Meta:
        model = Order
        fields = [
            "id",
            "date_created",
            "date_deliverd",
            "order_status",
            "total_price",
            "images",
        ]
        read_only_fields = ("date_created", "date_deliverd", "order_status", "cart")


class OrderProductsSerializer(serializers.ModelSerializer):
    products = WishlistSerializer(read_only=True)

    class Meta:
        model = OrderProducts
        fields = ["products", "quantity"]


class OrderDetailSerializer(serializers.ModelSerializer):
    user_address = serializers.SerializerMethodField()
    supplier_locations = serializers.SerializerMethodField()
    order = OrderProductsSerializer(many=True)

    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            "order",
            "order__products",
            "order__products__size",
            "order__products__color",
            "order__products__product",
        )
        return queryset

    def get_user_address(self, obj):
        add = obj.order_address
        return [add.latitude, add.longitude]

    def get_supplier_locations(self, obj):
        products = obj.order.values_list("products")
        supppliers_loc = SupplierProfile.objects.filter(
            product__product_detail__in=products
        ).distinct()

        return [(s.latitude, s.longitude) for s in supppliers_loc]

    class Meta:
        model = Order
        fields = [
            "id",
            "date_created",
            "date_deliverd",
            "order_status",
            "user_address",
            "supplier_locations",
            "order",
        ]
        read_only_fields = ("date_created", "date_deliverd", "order_status", "cart")



class DriverOrderSerializer(serializers.ModelSerializer):
    user_addresss = AddressSerializer(read_only = True)

    def get_supplier_locations(self, obj):  
        products = obj.order.values_list("products")
        suppliers = SupplierProfile.objects.filter(
            product__product_detail__in=products
        ).distinct()
        locations = {}
        locations['start'] = (self.context.get('long'),self.context.get('lat'))
        locations['end'] = (obj.order_address.longitude, obj.order_address.latitude)
        for supplier in suppliers:
            locations[supplier] = (supplier.longitude,supplier.latitude)
        
        distance = calculate_shortest_distance(locations)
        return distance



    class Meta:
        model = Order
        fields = [
            'id',
            'date_created',
            'user_address',
            'supplier_locations'
        ]



class DriverDetailedOrderSerializer(serializers.ModelSerializer):
    supplier_location = serializers.SerializerMethodField()
    user_addresss = AddressSerializer(read_only = True)

    def get_supplier_locations(self, obj):  
        products = obj.order.values_list("products")
        suppliers = SupplierProfile.objects.filter(
            product__product_detail__in=products
        ).distinct()
        serializer = OrderSupplierSerializer(instance=suppliers,many = True)

        return serializer.data

    class Meta:
        model = Order
        fields = [
            'id',
            'date_created',
            'user_address',
            'supplier_locations'
        ]
