from django.shortcuts import render
from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
import ast
from rest_framework.views import APIView
from .models import (
    Category,
    SupplierProfile,
    Product,
    Stock,
    ProductDetail,
    Brand,
    ImagesMaterializedView,
    ProductAttrsMaterializedViews
)
from .serializers import (
    ProductRegisterSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    ProductDetailSerializer,
    StockSerializer,
    ImagesMaterializedViewSerializer,
    ProductAttrsMaterializedViewSerializer
)
from django.db import transaction
from catalog.tasks import save_product_details
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


# Create your views here.
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
            supplier = SupplierProfile.objects.get(user=request.user)
            serializer = ProductRegisterSerializer(
                data=request.data,
                context={
                    "supplier": supplier,
                    "category": category,
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
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (Category.DoesNotExist, Category.DoesNotExist) as e:

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
        ).first()
        serializer = ProductSerializer(product, data=request.data, partial=True)
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
        product_qs = ProductWithReviewsSerializer.setup_eager_loading(
            Product.objects.filter(slug=slug)
        )
        product = product_qs.first()

        if not product:
            return Response({"error": "Product not found"}, status=404)

        product_images = ImagesMaterializedView.objects.filter(product_id=product.id)
        product_attrs = ProductAttrsMaterializedViews.objects.filter(product_id = product.id)
        product_serializer = ProductWithReviewsSerializer(product)

        return Response(
            {
                "product": product_serializer.data,
                "images": ImagesMaterializedViewSerializer(
                    product_images, many=True
                ).data,
                'attrs':ProductAttrsMaterializedViewSerializer(
                    product_attrs,many = True
                ).data
            }
        )


class ProductDetailDetail(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def put(self, request, pk, format=None):
        print
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

    def put(self, request, pk, format=None):
        stock = Stock.objects.get(pk=pk)
        serializer = StockSerializer(
            instance=stock, data=request.data, context=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "stock data updated"})

    def delete(self, request, pk, format=None):
        stocks = Stock.objects.get(id=pk)
        stocks.delete()


class FilterParams(APIView):

    def post(self, request, format=None):
        category = Category.objects.filter(slug=request.data["category"]).first()
        if category:
            products_with_brands = (
                Product.objects.filter(category=category)
                .select_related("brand")
                .values_list("pk", "brand__pk")
            )
            product_pks = [product[0] for product in products_with_brands]
            brand_pks = [product[1] for product in products_with_brands]
            brands = Brand.objects.filter(pk__in=brand_pks)
            serializer = BrandSerializer(instance=brands, many=True)
            sizes = Size_Value.objects.filter(
                productdetail__product__in=product_pks
            ).distinct()
            size_serializer = ProductSizeValueSerializer(instance=sizes, many=True)
            return Response({"brands": serializer.data, "sizes": size_serializer.data})
        else:
            product = Product.objects.filter(product_detail__size__pk=4)
            print(product)
            return Response({"no category found"})


class StartUpList(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None, *args, **kwargs):
        category = Category.objects.filter(level=0)
        serializer = CategorySerializer(instance=category, many=True)
        promotion = Promotion.objects.all()[:3]
        promotion_serializer = PromotionSerializer(
            instance=promotion, many=True, context={"request": request}
        )
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
