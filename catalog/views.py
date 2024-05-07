from .serializers import (
    ProductRegisterSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    ProductTypeSerializer,
    ProductDetailSerializer,
    ProductColorSerializer,
    ProductSizeSerializer,
    ProductSizeValueSerializer,
    ProductSerializer,
)
from .models import (
    Category,
    Product,
    ProductType,
    ProductColor,
    Size_Value,
    ProductDetail,
    Stock,
    ProductSize,
    ProductImage,
)
from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


class CategoryList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        name, desc, parent = request.data.values()

        if parent:
            parent = Category.objects.get(id=parent)

            category = Category.objects.create(
                name=name, description=desc, parent=parent
            )
        else:
            category = Category.objects.create(name=name, description=desc)
            return Response({"message": "created cat"}, status=status.HTTP_201_CREATED)
        return Response({"message": "bitch"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        category = Category.objects.filter(level=0)
        serializer = CategorySerializer(instance=category, many=True)
        return Response({"message": serializer.data})


class CategoryDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        category = self.get_object(slug)
        categories = category.get_children()
        serializer = CategorySerializer(instance=categories, many=True)
        return Response({"message": serializer.data})

    def put(self, request, slug, format=None):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        category = self.get_object(slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductTypeList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        product_size = ProductSize.objects.filter(
            size_type=request.data["product_size"]
        )
        serializer = ProductTypeSerializer(
            data=request.data, context={"product_size": product_size}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductTypeDetail(APIView):

    def get(self, request, name, format=None):
        size_values = Size_Value.objects.filter(size__product_size__name=name)
        serializer = ProductSizeValueSerializer(instance=size_values, many=True)
        return Response(serializer.data)


class ProductSizeList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = ProductSizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSizeValueList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        size = ProductSize.objects.filter(id=request.data["size"])
        serializer = ProductSizeValueSerializer(
            data=request.data, context={"size": size}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductColorList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = ProductColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        colors = ProductColor.objects.all()
        serailizer = ProductColorSerializer(data=colors, many=True)
        return Response(serailizer.data)


# remember to create a manageres for category and product to only get the active products
class ProductList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def post(self, request, format=None):
        category = Category.objects.get(id=request.data["category"])
        product_type = ProductType.objects.get(id=request.data["product_type"])
        user = request.user

        serializer = ProductRegisterSerializer(
            data=request.data,
            context={
                "supplier": request.user,
                "category": category,
                "product_type": product_type,
            },
        )
        if serializer.is_valid():
            product = serializer.save()
            colors = ProductColor.objects.filter(id__in=request.data["colors"])
            sizes = Size_Value.objects.filter(id__in=request.data["sizes"])
            counter = 0
            quantity_in_stock = request.data["qis"]
            if colors:
                for color in colors:
                    if sizes:
                        for size in sizes:
                            product_detail = ProductDetail.objects.create(
                                product=product
                            )
                            product_detail.size.add(size)
                            product_detail.color.add(color)
                            product_detail.save()
                            Stock.objects.create(
                                product_detail=product_detail,
                                quantity_in_stock=quantity_in_stock[counter],
                            )
                            counter = counter + 1

            return Response(
                {"message": "product created"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def get(self, request, slug, format=None):
        category = Category.objects.filter(slug=slug)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug)
        product.delete()
        return Response(
            {"message": "product deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class ProductDetailList(APIView):

    def get(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug)
        product_detail = ProductDetail.objects.filter(product=product)
        serializer = ProductDetailSerializer(instance=product_detail, many=True)
        return Response(serializer.data)


class ProductDetailDetail(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def put(self, request, pk, format=None):
        product_detail = ProductDetail.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product detail updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_detail = ProductDetail.objects.get(pk=pk)
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
