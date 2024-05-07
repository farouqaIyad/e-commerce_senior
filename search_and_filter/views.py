from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class SearchList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        return Response("hi", status=status.HTTP_400_BAD_REQUEST)
