from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from .models import Category,SubCategory,Product
from django.db import transaction
from rest_framework import status
from .utils import save_and_return_response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product(request):
    category = Category.objects.get(id = request.data['category'])
    subcategory_id = request.data['sub_category']
    serializer = ProductSerializer(data=request.data,context = {'supplier':request.user,'category':category})
    if serializer.is_valid():
        with transaction.atomic():
            product = serializer.save()
            product.sub_category.set(subcategory_id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(["get"])
@permission_classes([IsAuthenticated])
def view_product(request,pk):
    product = Product.objects.get(id = pk)
    serializer = ProductSerializer(instance=product)
    return Response(serializer.data)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def view_products(request):
    pass

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_subcategory(request):
    category = Category.objects.get(id = request.data['category'])
    serializer = SubCategorySerializer(data=request.data,context = {'category':category})
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

