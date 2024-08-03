from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import requests
from .models import Driver, DriverProfile
from .serializers import DriverProfileSerializer
from Users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from permissions import IsAdminOrReadOnly, IsDriver
from django.db import transaction
from fcm_django.models import FCMDevice
from rest_framework.parsers import MultiPartParser, FormParser


def index(request):

    return render(request, "driver/index.html")


def room(request, room_name):
    return render(request, "driver/room.html", {"room_name": room_name})


class DriverList(APIView):

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = DriverProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            try:
                with transaction.atomic():
                    user_data = user_serializer.validated_data
                    profile_data = profile_serializer.validated_data
                    user = Driver.objects.create_user(**user_data)
                    profile_data["user"] = user
                    driver_profile = DriverProfile.objects.create(**profile_data)
                    device = FCMDevice.objects.update_or_create(
                        registration_id=request.data["fcm_token"], user=user
                    )
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
            errors = {}
            errors.update(user_serializer.errors)
            errors.update(profile_serializer.errors)
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)


class DriverDetail(APIView):
    permission_classes = [IsDriver]

    def get(self, request, format=None):
        driver_serializer = DriverProfileSerializer(
            instance=request.user.driverprofile, context={"request": request}
        )
        return Response({"driver": driver_serializer.data})

    def put(self, request, format=None):
        serializer = DriverProfileSerializer(
            instance=request.user.driverprofile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "driver updated"})
        return Response(
            {"message": "couldn't update driver"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        driver = DriverProfile.objects.get(user=request.user)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApproveDriver(APIView):

    def post(self, request, format=None):
        supplier = DriverProfile.objects.get(pk=request.data["driver_id"])
        supplier.is_approved = request.data["is_approved"]
        supplier.save()
        return Response({"message": "driver approval status changed"})


class AdminViewDriver(APIView):

    def post(self, request, format=None):
        if "is_approved" in request.data:
            drivers = DriverProfile.objects.filter(
                is_approved=request.data["is_approved"]
            )
        else:
            drivers = DriverProfile.objects.all()
        serializer = DriverProfileSerializer(
            instance=drivers, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get(self, request, format=None):
        drivers = DriverProfile.objects.all()
        serializer = DriverProfileSerializer(
            instance=drivers, many=True, context={"request": request}
        )
        return Response(serializer.data)
