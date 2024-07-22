from .models import Order, Address, OrderProducts
from .serializers import OrderSerializer, AddressSerializer, OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from wishlist_cart.models import ShoppingCart
from django.db.models import Count, Q
from .tasks import return_to_stock
from datetime import datetime,timedelta


class AddressList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AddressSerializer(
            data=request.data, context={"customer": request.user.customerprofile}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        customer = request.user.customerprofile
        user_addresses = customer.address_set.all()
        serializer = AddressSerializer(user_addresses, many=True)
        return Response(serializer.data)


class AddressDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(instance=address)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address = get_object_or_404(Address, pk=pk)
        address.delete()
        return Response(status=status.HTTP_200_OK)


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        if user_shopping_cart.shopping_cart.all():
            address = self.get_object(pk=request.data["order_address"])
            serializer = OrderSerializer(
                data=request.data,
                context={"cart": user_shopping_cart, "order_address": address},
            )
            if serializer.is_valid():
                serializer.save()
                products = user_shopping_cart.shopping_cart.all()
                for product in products:
                    product.delete()
                return Response(
                    {"message": "order created"}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"message": "empty cart"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, format=None):
        orders = request.user.customerprofile.shoppingcart.cart.all()
        serializer = OrderSerializer(instance=orders, many=True)
        return Response({"orders": serializer.data})


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        order = Order.objects.filter(pk=pk)
        order = OrderDetailSerializer.setup_eager_loading(order)
        serializer = OrderDetailSerializer(instance=order[0])
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        if order.order_status == "Preprocessing":
            order.order_status = "Cancelled"
            order.save()    
            return_to_stock.delay()
            return Response({"message": "canceled your order"})
        else:
            return Response(
                {"message": "your order already {}".format(order.order_status)}
            )


class DriverOrderList(APIView):
    def get(self, request, format=None):
        # recieve long and lat from driver in request body
        # import geopy.distance
        # geopy.distance.geodesic(cord1,cord2).km)
        driver = request.user.driverprofile
        orders = Order.objects.filter(pick_up_method = driver.vehicle_type)[:10]
        seiralizer = OrderSerializer(instance=orders, many = True)

        # if orders:
        #     for order in orders:
        #         long = order.order_address.longitude
        #     two_days = datetime.now() + timedelta(days=2)
        #     late_orders = Order.objects.filter(order_status = 'Preprocessing',date_created__gte=two_days)[:5]

        
        return Response({"message":seiralizer.data})
