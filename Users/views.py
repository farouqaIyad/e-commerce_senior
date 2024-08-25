from .serializers import (
    UserSerializer,
    CustomerProfileSerializer,
)
from .models import (
    User,
    Customer,
    CustomerProfile,
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
from fcm_django.models import FCMDevice
from django.db import transaction


class CustomerSignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():

            try:
                with transaction.atomic():
                    user_data = user_serializer.validated_data
                    user = Customer.objects.create_user(**user_data)
                    customer_profile = CustomerProfile.objects.create(
                        user=user, phone_number=request.data["phone_number"]
                    )
                    # device = FCMDevice.objects.update_or_create(
                    #     registration_id=request.data["fcm_token"], user=user
                    # )
                    token = RefreshToken.for_user(user)
                    return Response(
                        {
                            "token": str(token.access_token),
                        },
                        status=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                return Response(f"An error occurred: {e}")

        else:

            return Response(
                {"message": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email_or_username = request.data["email"]
            password = request.data.get("password")

            if "@" in email_or_username:
                kwargs = {"email": email_or_username}
            else:
                kwargs = {"username": email_or_username}
            user = User.objects.get(**kwargs)
            if user and user.check_password(password):
                if "fcm_token" in request.data:
                    device = FCMDevice.objects.update_or_create(
                        registration_id=request.data["fcm_token"], user=user
                    )
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
        except:
            return Response(
                {"message": "failed to login"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        device = FCMDevice.objects.filter(user=request.user).first()
        if device:
            device.delete()
        return Response(status=status.HTTP_200_OK)


class AdminCustomersList(APIView):

    def get(self, request, format=None):
        customer = CustomerProfile.objects.all()
        customer = CustomerProfileSerializer.setup_eager_loading(customer)
        serializer = CustomerProfileSerializer(instance=customer, many=True)
        return Response({"customers": serializer.data}, status=status.HTTP_200_OK)


class AdminCustomerDetail(APIView):
    pass


class CustomerDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customer_serializer = CustomerProfileSerializer(
            instance=request.user.customerprofile, context={"request": request}
        )
        return Response({"customer": customer_serializer.data})

    def put(self, request, format=None):
        serializer = CustomerProfileSerializer(
            instance=request.user.customerprofile,
            data=request.data,
            partial=True,
            context=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer updated"})
        return Response(
            {"message": "couldn't update Customer"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, format=None):
        customer = CustomerProfile.objects.get(pk=20)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
