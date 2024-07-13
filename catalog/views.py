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
    ProductAttributeSerializer,
    ProductTypeAttributesSerializer,
    ProductAttributesvaluesSerializer,
    ProductWithReviewsSerializer,
    StockSerializer,
    BrandSerializer,
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
    ProductAttribute,
    ProductAttributeValues,
    ProductTypeAttributes,
    Brand,
    CategoriesBrand,
)
from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from promotion.serializers import Promotion, PromotionSerializer
from .tasks import save_product_details
from decimal import Decimal
import ast
from django.db.models import Avg, Max, Min, Sum


# admin
class CategoryList(APIView):

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
    # permission_classes = [IsAdminOrReadOnly]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        category = Category.objects.filter(slug=slug).first()
        categories = category.get_children()
        if categories:
            serializer = CategorySerializer(instance=categories, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "no children"})

    def put(self, request, slug, format=None):
        category = Category.objects.filter(slug=slug).first()
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category updated"})
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug, format=None):

        category = Category.objects.get(pk=request.data["category_id"])
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
            return Response(serializer.data)
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


class ProductAttributesList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = ProductAttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "created attribute"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "failed to create attribute"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductAttributesDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk, format=None):
        attribute = ProductAttribute.objects.get(pk=pk)
        try:
            attribute.delete()
            return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "failed to delete"}, status=status.HTTP_404_NOT_FOUND
            )


class ProductTypeAttributesList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        product_type = ProductType.objects.get(pk=request.data["product_type"])
        attribute = ProductAttribute.objects.get(pk=request.data["product_attribute"])
        serializer = ProductTypeAttributesSerializer(
            data=request.data,
            context={"product_type": product_type, "attribute": attribute},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "added attributes to type"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "failed to add "}, status=status.HTTP_400_BAD_REQUEST
        )


class ProductTypeAttributesDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk, format=None):
        product_type_attribute = ProductTypeAttributes.objects.get(pk=pk)
        try:
            product_type_attribute.delete()
            return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "failed to delete"}, status=status.HTTP_404_NOT_FOUND
            )


# supplier


class ProductList(APIView):
    permission_classes = [IsSupplierOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        try:
            category_id = request.data.get("category")
            product_type_id = request.data.get("product_type")
            colors_ids = request.data.get("colors", [])
            sizes_ids = request.data.get("sizes", [])
            quantity_in_stock = request.data.get("quantitiy_in_stock", [])
            prices_str = request.data.get("prices", [])
            prices = ast.literal_eval(prices_str)
            colors_ids = ast.literal_eval(colors_ids)
            sizes_ids = ast.literal_eval(sizes_ids)
            quantity_in_stock = ast.literal_eval(quantity_in_stock)
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

    def post(self, request, slug, format=None):
        category = Category.objects.filter(slug=slug).first()
        order = "-average_rating"
        if "new_arrival" in request.data:
            order = "-date_created"
        if "lowest_price" in request.data:
            order = "main_price"
        if "highest_price" in request.data:
            order = "-main_price"
        if category.is_leaf_node():
            products = (
                Product.objects.with_wishlist_status(request.user)
                .filter(category=category)
                .order_by(order)
            )

        else:
            child_categories = category.get_descendants()
            products = (
                Product.objects.with_wishlist_status(request.user)
                .filter(category__in=child_categories)
                .order_by(order)
            )

        serializer = ProductSerializer(instance=products, many=True)
        return Response({"products": serializer.data})

    def put(self, request, slug, format=None):
        product = Product.objects.filter(
            slug=slug, supplier=request.user.supplierprofile
        )
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
        product = Product.objects.filter(slug=slug)
        product = ProductWithReviewsSerializer.setup_eager_loading(product)
        product_serializer = ProductWithReviewsSerializer(product[0])

        return Response(
            {
                "product": product_serializer.data,
            }
        )


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


class SupplierPageList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def get(self, request, format=None):
        supplier = request.user.supplierprofile
        products = supplier.product_set.all()
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)


class StockList(APIView):

    def get(self, request, slug, format=None):
        stocks = Stock.objects.filter(product_detail__product__slug=slug)
        serializer = StockSerializer(instance=stocks, many=True)
        return Response({"stocks": serializer.data})


class StockDetail(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def put(self, request, pk, format=None):
        stock = Stock.objects.get(id=pk)
        serializer = StockSerializer(instance=stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": {"stock data updated"}})

    def delete(self, request, pk, format=None):
        stocks = Stock.objects.get(id=pk)
        stocks.delete()


# customer


class FilterParams(APIView):

    def post(self, request, format=None):
        category = Category.objects.filter(slug=request.data["category"]).first()
        brands = Brand.objects.filter(product__category=category).distinct()
        serializer = BrandSerializer(instance=brands, many=True)
        sizes = Size_Value.objects.filter(
            productdetail__product__category__slug=request.data["category"]
        ).distinct()
        size_serializer = ProductSizeValueSerializer(instance=sizes, many=True)

        return Response({"brands": serializer.data, "sizes": size_serializer.data})


class StartUpList(APIView):
    def get(self, request, format=None, *args, **kwargs):
        category = Category.objects.filter(level=0)
        serializer = CategorySerializer(instance=category, many=True)
        promotion = Promotion.objects.all()[:3]
        promotion_serializer = PromotionSerializer(instance=promotion, many=True)
        new_products = Product.objects.with_wishlist_status(request.user).order_by(
            "date_created"
        )[:10]

        new_products_serializer = ProductSerializer(instance=new_products, many=True)
        highest_rating_products = Product.objects.with_wishlist_status(
            request.user
        ).order_by("-average_rating")[:10]
        highest_rating_products_serializer = ProductSerializer(
            instance=highest_rating_products, many=True
        )

        return Response(
            {
                "categories": serializer.data,
                "promotion": promotion_serializer.data,
                "new products": new_products_serializer.data,
                "best_rating": highest_rating_products_serializer.data,
            }
        )
