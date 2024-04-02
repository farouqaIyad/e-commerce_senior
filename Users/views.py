from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .utils import extract_from_serializer
from rest_framework.views import APIView
from .serializers import UserSerializer,AddressSerializer
from django.db import transaction
from rest_framework import status
from django.http import Http404
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            email,password, first_name, last_name = extract_from_serializer(serializer)
            user = User.objects.create_admin(email= email,password = password,first_name = first_name,last_name = last_name)
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def customer_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def supplier_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            email,password, first_name, last_name = extract_from_serializer(serializer)
            user = User.objects.create_user(email= email,password = password,first_name = first_name,last_name = last_name,is_supplier = True)
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def driver_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            email,password, first_name, last_name = extract_from_serializer(serializer)
            user = User.objects.create_user(email= email,password = password,first_name = first_name,last_name = last_name,is_driver = True)
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def customer_supporter_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            email,password, first_name, last_name = extract_from_serializer(serializer)
            user = User.objects.create_user(email= email,password = password,first_name = first_name,last_name = last_name,is_superuser = True,is_staff = True)            
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
        print(user)
        return Response({"message":"{}".format(request.user.id)})

class AddressList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data,context = {'customer':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,format=None):
        user = request.user
        serializer = AddressSerializer(instance=user.address_set.all(),many = True)
        return Response(serializer.data)