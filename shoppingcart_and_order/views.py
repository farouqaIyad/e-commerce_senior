from .models import (
    Order,
    ShoppingCartProducts,
    ShoppingCart,
    ProductDetail,
    CustomerProfile,
)
from .serializers import (
    ShoppingCartSerializer,
    OrderSerializer,
    ShoppingCartProductsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import save_products_to_order
from rest_framework.views import APIView
from address.models import Address
from rest_framework import status
from django.http import Http404


class ShoppingCartList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        product = None
        if "product" in request.data and request.data["product"]:
            product = ProductDetail.objects.filter(
                product__id=request.data["product"], is_main=True
            ).first()
        elif "product_detail" in request.data:
            product = ProductDetail.objects.get(pk=request.data["product_detail"])
        _, created = ShoppingCartProducts.objects.get_or_create(
            shopping_cart=user_shopping_cart, product=product
        )
        if created:
            return Response(
                {"message": "added to cart"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "already added to cart"}, status=status.HTTP_201_CREATED
            )

    def get(self, request, format=None):
        cusotmerprofile = request.user.customerprofile
        user_shopping_cart = ShoppingCart.objects.filter(customer=cusotmerprofile)
        user_shopping_cart = ShoppingCartSerializer.setup_eager_loading(
            user_shopping_cart
        )
        serializer = ShoppingCartSerializer(instance=user_shopping_cart, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        products = user_shopping_cart.products.all()
        for product in products:
            user_shopping_cart.products.remove(product)
        return Response({"message": "shopping cart emptied"})


class ShoppingCartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        product = ShoppingCartProducts.objects.filter(
            shopping_cart=user_shopping_cart, product=pk
        ).first()
        product.quantity = request.data["quantity"]
        product.save()
        print(product.quantity)
        return Response({"message": "updated"})

    def delete(self, request, pk, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        product = self.get_object(pk=pk)
        user_shopping_cart.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistConvertToShoppingCart(APIView):

    def post(self, request, format=None):
        wishlist_products = request.user.customerprofile.wishlist.product.all()
        user_shoppingcart = request.user.customerprofile.shoppingcart
        for product in wishlist_products:
            _, created = ShoppingCartProducts.objects.get_or_create(
                shopping_cart=user_shoppingcart, product=product
            )
        return Response({"message": "converted from wishlist to shopping cart"})


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
