from .serializers import (
    UserSerializer,
    SupplierProfileSerializer,
    DriverProfileSerializer,
    CustomerProfileSerializer,
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
from permissions import IsAdminOrReadOnly


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
            customer_profile = CustomerProfile.objects.create(
                user=user, phone_number=request.data["phone_number"]
            )
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
                {"token": str(token.access_token), "role": user.role},
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


class SupplierList(APIView):

    def get(self, request, format=None):
        suppliers = SupplierProfile.objects.filter(user=1)
        serializer = SupplierProfileSerializer(instance=suppliers)
        return Response(serializer.data)


class SupplierDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, pk, format=None):
        supplier = SupplierProfile.objects.get(pk=pk)
        serializer = SupplierProfileSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "supplier updated"})
        return Response(
            {"message": "couldn't update supplier"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        supplier = SupplierProfile.objects.get(pk=pk)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerList(APIView):

    def get(self, request, format=None):
        customer = CustomerProfile.objects.all()[0]
        serializer = CustomerProfileSerializer(instance=customer)
        return Response({"customers": serializer.data}, status=status.HTTP_200_OK)


class CustomerDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, pk, format=None):
        customer = CustomerProfile.objects.get(pk=pk)
        serializer = CustomerProfileSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer updated"})
        return Response(
            {"message": "couldn't update Customer"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        customer = CustomerProfile.objects.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverList(APIView):

    def get(self, request, format=None):
        drivers = DriverProfile.objects.all()
        serializer = DriverProfileSerializer(instance=drivers, many=True)
        return Response(serializer.data)


class DriverDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, pk, format=None):
        Driver = DriverProfile.objects.get(pk=pk)

        serializer = DriverProfileSerializer(Driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "driver updated"})
        return Response(
            {"message": "couldn't update driver"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        supplier = SupplierProfile.objects.get(pk=pk)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
