from rest_framework.response import Response
from django.db import transaction
from rest_framework import status

def save_and_return_response(serializer):
    with transaction.atomic():
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED) 