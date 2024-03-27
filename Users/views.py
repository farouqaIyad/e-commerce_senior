from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .serializers import CustomerSerializer
from .models import Customer
from rest_framework import mixins
from rest_framework import generics

class CustomerView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
def view_something(request):
    return Response({'message':'hell world fkok'})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({'user_id': user.id,'token':str(token.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_users(request,pk):
        user = Customer.objects.get(id = pk)
        user_serializer = CustomerSerializer(user,many=False)
        return Response(user_serializer.data)


    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    user = request.user
    user.delete_user()
    return Response({"message":"Deleted User"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editProfile():
    pass


