from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from .serializers import (
    WishlistSerializer,
    ProductDetail,
    ShoppingCartProductsSerializer
)
from .models import ShoppingCartProducts, ShoppingCart
from catalog.models import Stock

class WishlistList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        user_wishlist = request.user.customerprofile.wishlist
        if "product" in request.data and request.data["product"]:
            product = ProductDetail.objects.filter(
                product__id=request.data["product"], is_main=True
            ).first()
        elif "product_detail" in request.data:
            product = ProductDetail.objects.get(pk=request.data["product_detail"])
        user_wishlist.product.add(product)
        user_wishlist.save()

        return Response(
            {"message": "added to wishlist"}, status=status.HTTP_201_CREATED
        )

    def get(self, request, format=None):
        user_wishlist = request.user.customerprofile.wishlist
        products_qs = WishlistSerializer.setup_eager_loading(user_wishlist.product)
        return Response(
            {"products": WishlistSerializer(instance=products_qs, many=True).data}
        )
    
    def delete(self, request, format=None):
        if "all" in request.data:
            user_wishlist = request.user.customerprofile.wishlist
            products = user_wishlist.product.all()
            for product in products:
                user_wishlist.product.remove(product)
            return Response({"message": "empty wishlist"})
        else:
            user_wishlist = request.user.customerprofile.wishlist
            if "product" in request.data and request.data["product"]:
                product = ProductDetail.objects.filter(
                    product__id=request.data["product"], is_main=True
                ).first()
            elif "product_detail" in request.data:
                product = ProductDetail.objects.get(pk=request.data["product_detail"])
            user_wishlist.product.remove(product)

        return Response(
            {"message": "deleted product from wishlist"}, status=status.HTTP_200_OK
        )


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
        shoppingcart = request.user.customerprofile.shoppingcart
        cart_products = ShoppingCartProducts.objects.filter(shopping_cart=shoppingcart)
        cart_products = ShoppingCartProductsSerializer.setup_eager_loading(
            cart_products
        )
        serializer = ShoppingCartProductsSerializer(instance=cart_products, many=True)
        return Response({"products":serializer.data,"total_price":int(shoppingcart.total_price)})


    def delete(self, request, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        if "all" in request.data:
            products = user_shopping_cart.shopping_cart.all()
            for product in products:
                product.delete()
            return Response({"message": "shopping cart emptied"})
        else:
            product = ProductDetail.objects.get(pk=request.data["product_detail"])
            product_in_cart = user_shopping_cart.shopping_cart.filter(product = product)
            product_in_cart.delete()
        return Response({"message": "deleted product"})


class ShoppingCartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404
    
    def get(self, request, pk,format =None):
        quantity = Stock.objects.filter(product_detail__id = pk).first()
        return Response({"quantity":quantity.quantity_in_stock})

    def put(self, request, pk, format=None):
        user_shopping_cart = request.user.customerprofile.shoppingcart
        product = ShoppingCartProducts.objects.filter(
            shopping_cart=user_shopping_cart, product=pk
        ).first()
        product.quantity = request.data["quantity"]
        product.save()
        return Response({"message": "updated"})



class WishlistConvertToShoppingCart(APIView):

    def post(self, request, format=None):
        wishlist_products = request.user.customerprofile.wishlist.product.all()
        user_shoppingcart = request.user.customerprofile.shoppingcart
        for product in wishlist_products:
            _, created = ShoppingCartProducts.objects.get_or_create(
                shopping_cart=user_shoppingcart, product=product
            )
        return Response({"message": "converted from wishlist to shopping cart"})


class Test(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
            user_shopping_cart = request.user.customerprofile.shoppingcart.shopping_cart.all()
            print(user_shopping_cart)
            # if "all" in request.data:
            #     cart_products = ShoppingCartProducts.objects.filter(shopping_cart=user_shopping_cart)
            #     for product in cart_products:
            #         product.delete()
            #     return Response({"message": "shopping cart emptied"})
            # else:
            #     product = ProductDetail.objects.get(pk=request.data["product_detail"])
            #     obj = ShoppingCartProducts.objects.filter(product = product,shopping_cart=user_shopping_cart).first()
            #     obj.delete()
            return Response({"message": "deleted product"})