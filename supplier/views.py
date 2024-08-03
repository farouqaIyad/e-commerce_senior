from django.shortcuts import render
from .serializers import (
    UserSerializer,
    SupplierProfileSerializer,
    SupplierProfile,
    Supplier,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from permissions import IsAdminOrReadOnly, IsSupplierOrReadOnly
from catalog.serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class SupplierSignupAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            user_serializer = UserSerializer(data=request.data)
            profile_serializer = SupplierProfileSerializer(data=request.data)
            print("worked here")
            if user_serializer.is_valid() and profile_serializer.is_valid():
                user_data = user_serializer.validated_data
                profile_data = profile_serializer.validated_data
                user = Supplier.objects.create_user(**user_data)
                profile_data["user"] = user
                supplier_profile = SupplierProfile.objects.create(**profile_data)
                token = RefreshToken.for_user(user)

                return Response(
                    {
                        "token": str(token.access_token),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                errors = {}
                errors.update(user_serializer.errors)
                errors.update(profile_serializer.errors)
                print(user_serializer.errors)
                print(profile_serializer.errors)

                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            print(user_serializer.errors)
            return Response({"message":user_serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class SupplierList(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def put(self, request, format=None):
        serializer = SupplierProfileSerializer(
            request.user.supplierprofile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "supplier updated"})
        return Response(
            {"message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, format=None):
        supplier = SupplierProfile.objects.filter(user=request.user).first()
        # supplier.delete()
        return Response(
            {"message": "supplier deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class SupplierDetail(APIView):
    permission_classes = [IsSupplierOrReadOnly]

    def get(self, request, format=None):
        serializer = SupplierProfileSerializer(
            instance=request.user.supplierprofile, context={"request": request}
        )
        return Response(serializer.data)


class ApproveSupplier(APIView):

    def post(self, request, format=None):
        supplier = SupplierProfile.objects.get(pk=request.data["supplier_id"])
        supplier.is_approved = request.data["is_approved"]
        supplier.save()
        return Response({"message": "supplier approval state changed"})


class AdminViewSupplier(APIView):

    def post(self, request, format=None):
        if "is_approved" in request.data:
            supplier = SupplierProfile.objects.filter(
                is_approved=request.data["is_approved"]
            )
        else:
            supplier = SupplierProfile.objects.all()
        serializer = SupplierProfileSerializer(
            instance=supplier, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get(self, request, format=None):
        supplier = SupplierProfile.objects.all()
        serializer = SupplierProfileSerializer(
            instance=supplier, many=True, context={"request": request}
        )
        return Response(serializer.data)
