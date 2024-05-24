from .serializers import (
    UserSerializer,
    SupplierProfileSerializer,
    DriverProfileSerializer,
)
from .models import (
    User,
    Supplier,
    Customer,
    Driver,
    SupplierProfile,
    CustomerProfile,
    DriverProfile,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from .models import User


class SupplierSignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = SupplierProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_data = user_serializer.validated_data
            profile_data = profile_serializer.validated_data
            user = Supplier.objects.create_user(**user_data)
            profile_data["user"] = user
            supplier_profile = SupplierProfile.objects.create(**profile_data)
            token = RefreshToken.for_user(user)

            return Response(
                {
                    "user": user_serializer.data,
                    "supplier_profile": SupplierProfileSerializer(
                        supplier_profile
                    ).data,
                    "token": str(token.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = {}
            errors.update(user_serializer.errors)
            errors.update(profile_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "user deleted {}".format(user)})


class CustomerSignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_data = user_serializer.validated_data
            user = Customer.objects.create_user(**user_data)
            customer_profile = CustomerProfile.objects.create(user=user)
            token = RefreshToken.for_user(user)

            return Response(
                {
                    "user": user_serializer.data,
                    "token": str(token.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = {}
            errors.update(user_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "user deleted {}".format(user)})


class DriverSignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = DriverProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_data = user_serializer.validated_data
            profile_data = profile_serializer.validated_data
            user = Driver.objects.create_user(**user_data)
            profile_data["user"] = user
            driver_profile = DriverProfile.objects.create(**profile_data)
            token = RefreshToken.for_user(user)

            return Response(
                {
                    "user": user_serializer.data,
                    "driver_profile": DriverProfileSerializer(driver_profile).data,
                    "token": str(token.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = {}
            errors.update(user_serializer.errors)
            errors.update(profile_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "user deleted {}".format(user)})


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data.get("password")
        user = User.objects.get(email=email)
        if user and user.check_password(password):
            token = RefreshToken.for_user(user)
            message = "logged in as a {}".format(user.role)
            return Response(
                {"message": message, "token": str(token.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "incorrect email or password."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    print(user)
    return Response({"message": "{}".format(request.user.id)})
