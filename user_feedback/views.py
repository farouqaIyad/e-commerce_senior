from .serializers import ReviewSerializer,ComplaintsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Product
from rest_framework import status
from django.db import transaction
from django.http import Http404


class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data['product_id']
        product = Product.objects.get(id = product_id)
        serializer = ReviewSerializer(data=request.data,context = {'customer':request.user,'product':product})
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
        product_id = request.data['product_id']
        product = Product.objects.get(id = product_id)
        serializer = ReviewSerializer(data=request.data,context = {'customer':request.user,'product':product})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_complaint(request):
    serializer = ComplaintsSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        pass
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)