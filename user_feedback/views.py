from .serializers import ReviewSerializer,ComplaintsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)

class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data,context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_complaint(request):
    serializer = ComplaintsSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        save_and_return_response(serializer)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)