from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import WishlistSerializer
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from .models import Wishlist


class WishlistList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        user_wishlist = request.user.wishlist
        product = self.get_object(request.data["product"])
        user_wishlist.product.add(product)
        user_wishlist.save()
        return Response(
            {"message": "added to wishlist"}, status=status.HTTP_201_CREATED
        )

    def get(self, request, format=None):
        user_wishlist = request.user.wishlist
        serializer = WishlistSerializer(instance=user_shoppingcart)
        return Response(serializer.data)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user_wishlist = request.user.wishlist
        product = self.get_object(pk=pk)
        user_wishlist.product.delete(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
