from .models import Order, Address
from .serializers import OrderSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404


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
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        address = self.get_object(pk=request.data["order_address"])
        serializer = OrderSerializer(
            data=request.data,
            context={"shopping_cart": user_shopping_cart, "order_address": address},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        order = Order.objects.select_related("shopping_cart").get(
            shopping_cart__customer__user=request.user
        )

        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)
