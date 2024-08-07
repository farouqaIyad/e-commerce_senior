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
from .models import (
    Coupon,
    Promotion,
    Product,
    SupplierProfile,
    ProductOnPromotion,
    ProductDetail,
)
from rest_framework.parsers import MultiPartParser, FormParser


class CouponList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def post(self, request, format=None):
        serializer = CouponSerializer(
            data=request.data, context={"supplier": request.user.supplierprofile}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        coupons = Coupon.objects.filter(supplier=request.user.supplierprofile)
        serializer = CouponSerializer(instance=coupons, many=True)
        return Response(serializer.data)


class CouponDetail(APIView):

    def put(self, request, pk, format=None):
        coupon = Coupon.objects.get(pk=pk)
        serializer = CouponSerializer(instance=coupon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "coupon updated"})
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        coupon = Coupon.objects.get(pk=pk)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UseCoupon(APIView):
    def post(self, request, format=None):
        coupon = Coupon.objects.filter(
            coupon_code=request.data["coupon_code"], is_active=True
        ).first()
        if coupon:
            serializer = CouponSerializer(instance=coupon)
            return Response({"coupon": serializer.data})
        else:
            return Response(
                {"coupon": "no valid coupon matching the coupon code you entered"}
            )


class PromotionList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        promotions = Promotion.objects.all()
        serializer = PromotionSerializer(
            instance=promotions, many=True, context={"request": request}
        )
        return Response({"promotions": serializer.data})


class PromotionDetail(APIView):
    def put(self, request, pk, format=None):
        promotion = Promotion.objects.get(pk=pk)
        serializer = PromotionSerializer(
            instance=promotion, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "promotion updated"})
        return Response(
            {"message": "failed to update"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        promotion = Promotion.objects.get(pk=pk)
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PromotionFilter(APIView):
    def post(self, request, format=None):
        promotions = Promotion.objects.filter(is_active=request.data["is_active"])
        serializer = PromotionSerializer(instance=promotions, many=True)
        return Response(serializer.data)


class ProductOnPromotionList(APIView):
    def post(self, request, pk, format=None):
        products = request.data.get("products", [])
        products = Product.objects.filter(pk__in=products)
        promotion = Promotion.objects.get(pk=pk)
        with transaction.atomic():
            for product in products:
                ProductOnPromotion.objects.create(promotion=promotion, product=product)
        return Response({"Message": "product added to promotions"})

    def get(self, request, pk, format=None):
        products = Product.objects.with_wishlist_status(request.user).filter(
            products_on_promotion__promotion_id=pk
        )
        serializer = ProductSerializer(instance=products, many=True)
        return Response({"products": serializer.data})
