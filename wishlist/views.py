from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import WishlistSerializer
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from .models import Wishlist, ProductDetail
from Users.models import CustomerProfile

class WishlistList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        customer = CustomerProfile.objects.get(user_id = request.user.id)
        user_wishlist = Wishlist.objects.get(customer = customer)
        product_detail = request.data["product_detail"]
        #product = request.data["product"]
        """if product:
            product = ProductDetail.objects.filter(product__id=product, is_main=True)"""
        product = self.get_object(product_detail)
        user_wishlist.product.add(product)
        user_wishlist.save()
        return Response(
            {"message": "added to wishlist"}, status=status.HTTP_201_CREATED
        )

    def get(self, request, format=None):
        customer = CustomerProfile.objects.get(user_id = request.user.id)
        user_wishlist = Wishlist.objects.get(customer = customer)
        serializer = WishlistSerializer(instance=user_wishlist)
        return Response(serializer.data)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user_wishlist = request.user.wishlist
        product = self.get_object(pk=pk)
        user_wishlist.product.delete(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
