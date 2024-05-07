from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DealsSerializer
from django.shortcuts import render
from rest_framework import status
from django.http import Http404


class DealsList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        supplier = request.user
        serializer = DealsSerializer(
            data=request.data,
            context={"supplier": supplier, "products": request.data["products"]},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        supplier_deals = request.user.deals_set.all()
        serializer = DealsSerializer(instance=supplier_deals, many=True)
        return Response(serializer.data)
