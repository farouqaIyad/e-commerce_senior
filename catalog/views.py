from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category,SubCategory,Product
from django.db import transaction
from rest_framework import status
from .utils import save_and_return_response
from django.http import Http404

class ProductList(APIView):
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Pr.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        products = category.products.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
def get_product_details(request,pk):
    product = Product.objects.get(id = pk)
    serializer = ProductSerializer(instance=product)
    return Response(serializer.data)

class CategoryList(APIView):
    
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        products = category.products.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SubCategoryList(APIView):
    
    def get(self, request, format=None):
        subcategory = SubCategory.objects.all()
        serializer = CategorySerializer(subcategory, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubCategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subcategory = self.get_object(pk)
        products = subcategory.products.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    


