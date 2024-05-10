from permissions import IsSupplierOrReadOnly, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CouponSerializer
from .models import Coupon, SupplierProfile


class CouponList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def post(self, request, format=None):
        supplier_profile = SupplierProfile.objects.get(pk=request.user)
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


class CouponList(APIView):
    pass
