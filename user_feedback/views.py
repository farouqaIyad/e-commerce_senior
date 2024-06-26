from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Product
from rest_framework import status
from django.http import Http404
from .models import Review


class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data["product"]
        product = Product.objects.get(id=product_id)
        serializer = ReviewSerializer(
            data=request.data,
            context={"customer": request.user.customerprofile, "product": product},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
