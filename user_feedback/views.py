from .serializers import ReviewSerializer,ComplaintsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from catalog.utils import save_and_return_response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_complaint(request):
    serializer = ComplaintsSerializer(data=request.data,context = {'request':request})
    if serializer.is_valid():
        save_and_return_response(serializer)
    return Response({"message":serializer.erros},status=status.HTTP_400_BAD_REQUEST)