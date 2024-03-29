from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.http import Http404


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data['email']
    password = request.data.get('password')
    user = User.objects.get(email = email)
    if user and user.check_password(password):
        token = RefreshToken.for_user(user)
        return Response({"message":'login successful',"token":str(token.access_token)},status=status.HTTP_200_OK)
    return Response({"message":"incorrect email or password."},status=status.HTTP_400_BAD_REQUEST)
         
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_account(request):
        user = request.user
        user.delete_user()
        return Response({"message":"{}".format(request.user)})




