from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer, ComplaintsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Product
from rest_framework import status
from django.http import Http404


class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data["product"]
        product = Product.objects.get(id=product_id)
        serializer = ReviewSerializer(
            data=request.data, context={"customer": request.user, "product": product}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComplaintList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        order_id = request.data["order_id"]
        order = Order.objects.get(id=order_id)
        serializer = ComplaintsSerializer(
            data=request.data, context={"customer": request.user, "order": order}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user = request.user
        serializer = ComplaintsSerializer(user.complaints_set.all(), many=True)
        return Response(serializer.data)
