from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    CouponSerializer,
    PromotionSerializer,
    ProductOnPromotionSerializer,
)
from catalog.serializers import ProductSerializer
from django.db import transaction
from .models import Coupon, Promotion, Product, SupplierProfile, ProductOnPromotion
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize


class CouponList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def post(self, request, format=None):
        supplier_profile = SupplierProfile.objects.get(pk=request.user.id)
        serializer = CouponSerializer(
            data=request.data, context={"supplier": supplier_profile}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        supplier_profile = SupplierProfile.objects.get(pk=request.user)
        coupons = SupplierProfile.objects.filter(supplier=supplier_profile)
        serializer = CouponSerializer(instance=coupons, many=True)


class CouponDetail(APIView):

    def post(self, request, pk, format=None):
        coupon = Coupon.objects.filter(coupon_code=request.data["coupon_code"]).first()
        return Response({"message": coupon.discount_value})


class PromotionList(APIView):

    def post(self, request, format=None):
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        promotions = Promotion.objects.all()
        serializer = PromotionSerializer(instance=promotions, many=True)
        return Response(serializer.data)


class PromotionDetail(APIView):
    def put(self, request, pk, format=None):
        promotion = Promotion.objects.get(pk=pk)
        serializer = PromotionSerializer(instance=promotion, data=request.data)
        if serializer.is_valid():
            serialize.save()
            return Response({"message": "product updated"})
        return Response(
            {"message": "failed to update"}, status=status.HTTP_400_BAD_REQUEST
        )


class ProductOnPromotionList(APIView):
    def post(self, request, pk, format=None):
        products = request.data.get("products", [])
        products = Product.active_products.filter(pk__in=products)
        promotion = Promotion.objects.get(pk=pk)
        with transaction.atomic():
            for product in products:
                ProductOnPromotion.objects.create(promotion=promotion, product=product)
        return Response({"Message": "product added to promotions"})

    def get(self, request, pk, format=None):
        products = Product.active_products.filter(product_on_promotion__promotion_id=pk)
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)
