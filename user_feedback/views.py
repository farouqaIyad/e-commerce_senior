from .serializers import (
    ReviewSerializer,
    ReturnalSerializer,
    ReturnReasonSerializer,
    ReturnMethodSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .models import Review, Returnal, ProductDetail, ReturnReason, ReturnMethod
from rest_framework.response import Response
from rest_framework.views import APIView
from inventory.models import Product
from rest_framework import status
from django.http import Http404


class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data["product"]
        product = Product.objects.get(id=product_id)
        serializer = ReviewSerializer(
            data=request.data,
            context={"customer": request.user.customerprofile, "product": product},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReturnReasonList(APIView):
    def get(self, request, format=None):
        reasons = ReturnReason.objects.all()
        serializer = ReturnReasonSerializer(instance=reasons, many=True)
        return Response({"reasons": serializer.data})


class ReturnMethodDetail(APIView):
    def get(self, request, pk, format=None):
        methods = ReturnMethod.objects.filter(return_reason=pk)
        serializer = ReturnMethodSerializer(instance=methods, many=True)
        return {"methods": serializer.data}


class ReturnalList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        customer = request.user.customerprofile
        product_detail = ProductDetail.objects.get(pk=request.data["product_detail"])
        serializer = ReturnalSerializer(
            data=request.data,
            context={"customer": customer, "product_detail": product_detail},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "return request created successfully"},
                status=status.HTTP_201_CREATED,
            )

    def get(self, request, format=None):
        customer = request.user.customerprofile
        returnals = Returnal.objects.filter(customer=customer)
        serializer = ReturnalSerializer(instance=returnals, many=True)
        return Response({"returnals": serializer.data})


class SupplierReturnal(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        supplier = request.user.supplierprofile
        returnals = Returnal.objects.filter(
            product_detail__product__supplier=supplier
        ).prefetch_related("product_detail")
        serializer = ReturnalSerializer(instance=returnals, many=True)
        return Response({"returnals": serializer.data})


class SupplierReturnalDetail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        returnal = Returnal.objects.get(pk=pk)
        returnal.is_approved = request.data["approved"]
        returnal.save()
        return Response({"message": "approved"})
