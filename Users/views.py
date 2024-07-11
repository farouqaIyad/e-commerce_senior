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

    def get(self, request, format=None):
        print(request.data)
        return Response({"message": "hello"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user.customerprofile
    user.delete()

    return Response({"message": "customer deleted"}, status=status.HTTP_204_NO_CONTENT)


class CustomerList(APIView):

    def get(self, request, format=None):
        customer = CustomerProfile.objects.all()
        customer = CustomerProfileSerializer.setup_eager_loading(customer)
        serializer = CustomerProfileSerializer(instance=customer, many=True)
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
