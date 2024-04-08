from .serializers import ShoppingCartSerializer,Product,OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from address.models import Address
from rest_framework import status
from django.http import Http404
from .models import Order


class ShoppingCartList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, format = None):
        user_shoppingcart = request.user.shoppingcart
        product = self.get_object(request.data['product'])  
        user_shoppingcart.product.add(product)    
        user_shoppingcart.save()
        return Response({"message":"added to cart"},status=status.HTTP_201_CREATED)    
    
    def get(self,request,format = None):
        user_shoppingcart = request.user.shoppingcart
        serializer = ShoppingCartSerializer(instance=user_shoppingcart)
        return Response(serializer.data)

class ShoppingCartDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format = None):
        user_shoppingcart = request.user.shoppingcart
        product = self.get_object(pk = pk)
        user_wishlist.product.delete(product)
        return Response(status = status.HTTP_204_NO_CONTENT)
    

class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def post(self,request,format = None):
        user_shoppingcart = request.user.shoppingcart
        address = self.get_object(pk = request.data['address_id'])
        order = Order.objects.create(customer = request.user, order_address = address )
        order.product.add(*user_shoppingcart.product.all())
        order.save()
        return Response({"message":"order created"})
    
    def get(self,request,format = None):
        order = request.user.order_set.all()
        serializer = OrderSerializer(instance = order, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)



