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
    ProductPageSerializer,
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
    SupplierProfile,
)
from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .tasks import save_product_details


class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        name, parent = request.data.values()
        try:
            if parent:
                parent = Category.objects.get(id=parent)

                category = Category.objects.create(name=name, parent=parent)
                return Response(
                    {"message": "created category"}, status=status.HTTP_201_CREATED
                )

            elif not parent:
                category = Category.objects.create(name=name)
                return Response(
                    {"message": "created category"}, status=status.HTTP_201_CREATED
                )
        except:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        category = Category.objects.filter(level=0)
        serializer = CategorySerializer(instance=category, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        category = Category.objects.filter(slug=slug)
        categories = category.get_children()
        if categories:
            serializer = CategorySerializer(instance=categories, many=True)
            return Response({"message": serializer.data})
        else:
            return Response({"message": "no children"})

    def put(self, request, slug, format=None):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category updated"})
        return Response(
            {"message": "could not update category"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug, format=None):
        category = self.get_object(slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductTypeList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        product_size = ProductSize.objects.get(pk=request.data["product_size"])
        category = Category.objects.get(pk=request.data["category"])
        if not category.is_leaf_node():
            return Response(
                {"message": "cannot add a type to a category that has children"}
            )

        serializer = ProductTypeSerializer(
            data=request.data,
            context={"product_size": product_size, "category": category},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ProductTypeDetail(APIView):

    def get(self, request, slug, format=None):
        try:

            types = ProductType.objects.filter(category__slug=slug).prefetch_related(
                "category"
            )
            serializer = ProductTypeSerializer(instance=types, many=True)
            return Response({"message": serializer.data})
        except:
            return Response({"message": "error"})


class ProductSizeList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = ProductSizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ProductSizeValueList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        try:
            size = ProductSize.objects.filter(product_size=request.data["size"]).first()
            value = request.data["value"]
            size_value = Size_Value.objects.create(size=size, value=value)
            size_value.save()

            return Response(
                {"message": "size value added"}, status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {"message": "error occured"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProductSizeValueDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, name, format=None):
        try:
            size_values = Size_Value.objects.filter(
                size__producttype__name=name
            ).select_related("size")
            serializer = ProductSizeValueSerializer(instance=size_values, many=True)
            return Response({"message": serializer.data})
        except:
            return Response({"message": "an error occured"})


class ProductColorList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = ProductColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, format=None):
        colors = ProductColor.objects.all()
        serailizer = ProductColorSerializer(instance=colors, many=True)
        return Response(serailizer.data)


class ProductList(APIView):
    permission_classes = [IsSupplierOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        try:
            category_id = request.data.get("category")
            product_type_id = request.data.get("product_type")
            colors_ids = request.data.get("colors", [])
            sizes_ids = request.data.get("sizes", [])
            quantity_in_stock = request.data.get("quantitiy_in_stock", [])
            prices = request.data.get("prices", [])
            # images = request.data.get("images", [])

            category = Category.objects.get(id=category_id)
            product_type = ProductType.objects.get(id=product_type_id)
            supplier = SupplierProfile.objects.get(user=request.user)
            serializer = ProductRegisterSerializer(
                data=request.data,
                context={
                    "supplier": supplier,
                    "category": category,
                    "product_type": product_type,
                },
            )
            if serializer.is_valid():
                with transaction.atomic():
                    product = serializer.save()
                    save_product_details.delay(
                        product.id, quantity_in_stock, prices, colors_ids, sizes_ids
                    )
                return Response(
                    {"message": "Product created"}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (Category.DoesNotExist, ProductType.DoesNotExist) as e:
            return Response(
                {"message": "One or more entities not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductDetailView(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def get(self, request, slug, format=None):
        category = Category.objects.filter(slug = slug).first()
        if category.is_leaf_node():
            products = Product.objects.filter(category=category)
        else:
            child_categories = category.get_descendants()
            products = Product.objects.filter(category__in = child_categories)
            print(products)
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)

        # return Response(serializer.data)

    def put(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product updated"})
        return Response(
            {"message": "failed to update"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        product.delete()
        return Response(
            {"message": "product deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class ProductDetailList(APIView):

    def get(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        serializer = ProductPageSerializer(instance=product)
        return Response(serializer.data)


class ProductDetailDetail(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def put(self, request, pk, format=None):
        product_detail = ProductDetail.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product detail updated"})
        return Response(
            {"message": "couldn't update product details"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        product_detail = ProductDetail.objects.get(pk=pk)
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
