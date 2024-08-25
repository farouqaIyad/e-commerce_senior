from .models import Order, Address, OrderProducts
from .serializers import (
    OrderSerializer,
    AddressSerializer,
    OrderDetailSerializer,
    DriverOrderSerializer,
    DriverDetailedOrderSerializer,
    DeliverSeializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from wishlist_cart.models import ShoppingCart
from .tasks import return_to_stock
from django.db import transaction
from datetime import datetime


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
    def post(self, request, format=None):
        from .serializers import DriverOrderSerializer

        driver = request.user.driverprofile
        orders = Order.objects.filter(
            pick_up_method=driver.vehicle_type,
            order_status="Preprocessing",
            driver=None,
        )[:10]
        if orders:
            seiralizer = DriverOrderSerializer(
                instance=orders,
                many=True,
                context={"lat": request.data["lat"], "long": request.data["long"]},
            )
            return Response({"message": seiralizer.data})
        else:
            return Response({"message": []})


class DriverOrderDetail(APIView):
    def get(self, request, pk, format=None):
        order = Order.objects.filter(pk=pk)
        order = DriverDetailedOrderSerializer.setup_eager_loading(order)
        serializer = DriverDetailedOrderSerializer(instance=order[0])
        return Response(serializer.data)


class MyOrders(APIView):
    def post(self, request, format=None):
        order = Order.objects.filter(driver=request.user.driverprofile)
        serializer = DriverOrderSerializer(
            instance=order,
            many=True,
            context={"lat": request.data["lat"], "long": request.data["long"]},
        )
        return Response({"message": serializer.data})


class DriverFlagPickedUp(APIView):
    def post(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        with transaction.atomic():
            order.order_status = "Picked up"
            order.driver = request.user.driverprofile
            order.save()
        return Response({"message": "picked up the order"})


class DriverFlagDelivered(APIView):
    def post(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        serializer = DeliverSeializer(
            instance=order, data=request.data, context=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "deliverd"})
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class order_test(APIView):
    def get(self, request, format=None):
        # from .tasks import add_product_bought_from_supplier
        # devices = FCMDevice.objects.filter(user__role="DRIVER")
        # if devices:
        #     title = "A New Order is Available"
        #     body = "open app to view order details"

        #     for device in devices:
        #         device.send_message(
        #         Message(
        #             notification=Notification(
        #                 title=title,
        #                 body=body,
        #             )
        #         )
        #     )
        # from driver.models import DriverProfile
        # from Users.models import User
        # users = User.objects.filter(role = "DRIVER")
        # counter = 1
        # for user in users:
        #     user.first_name = 'user{}'.format(counter)
        #     user.last_name = 'driver{}'.format(counter)
        #     user.save()
        #     counter+=1
        # # d= DriverProfile.objects.get(pk=1)
        # # d.user.first_name = 'yamen'
        # # d.user.last_name = 'al darwish'
        # # d.user.save()
        # # f= DriverProfile.objects.get(pk=2)
        # # f.user.first_name = 'farouq'
        # # f.user.last_name = 'aiyad'
        # # f.user.save()
        # # s= DriverProfile.objects.get(pk=3)
        # # s.user.first_name = 'siham'
        # # s.user.last_name = 'barakat'
        # # s.user.save()
        return Response({"message": "done"})
