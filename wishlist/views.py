from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from .serializers import WishlistSerializer, ProductDetail


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
        user_wishlist = request.user.customerprofile.wishlist
        products = user_wishlist.product.all()
        for product in products:
            user_wishlist.product.remove(product)
        return Response({"message": "empty wishlist"})


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user_wishlist = request.user.customerprofile.wishlist
        product = self.get_object(pk=pk)
        user_wishlist.product.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
