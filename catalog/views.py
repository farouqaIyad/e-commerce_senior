from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product(request):
    serializer = ProductSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_subcategory(request):
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)

