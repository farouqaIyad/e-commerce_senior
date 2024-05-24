from .models import (
    Order,
    ShoppingCartProducts,
    ShoppingCart,
    ProductDetail,
    CustomerProfile,
)
from .serializers import ShoppingCartSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import save_products_to_order
from rest_framework.views import APIView
from address.models import Address
from rest_framework import status
from django.http import Http404


class ShoppingCartList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        customer = CustomerProfile.objects.get(user=request.user)
        shopping_cart = ShoppingCart.objects.filter(customer=customer).first()
        product = self.get_object(request.data["product_id"])
        shopping_cart_products = ShoppingCartProducts.objects.create(
            shopping_cart=shopping_cart, product=product
        )
        shopping_cart_products.save()
        return Response({"message": "added to cart"}, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        customer = CustomerProfile.objects.get(user=request.user)
        shopping_cart = ShoppingCart.objects.filter(customer=customer).first()
        serializer = ShoppingCartSerializer(instance=shopping_cart)
        return Response(serializer.data)


class ShoppingCartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        shopping_cart = ShoppingCart.objects.get(pk=request.user)
        product = ShoppingCartProducts.objects.filter(
            shopping_cart=shopping_cart, product=pk
        ).first()
        product.quantity = request.data["quantity"]
        product.save()
        return Response({"message": "updated"})

    def delete(self, request, pk, format=None):
        shopping_cart = ShoppingCart.objects.get(pk=request.user)
        product = ShoppingCartProducts.objects.filter(
            shopping_cart=shopping_cart, product=pk
        ).first()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        shopping_cart = ShoppingCart.objects.get(customer__user=request.user)
        print(shopping_cart)
        address = self.get_object(pk=request.data["order_address"])
        serializer = OrderSerializer(
            data=request.data,
            context={"shopping_cart": shopping_cart, "order_address": address},
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
