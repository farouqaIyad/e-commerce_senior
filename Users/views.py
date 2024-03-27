from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .serializers import CustomerSerializer,AdminSerializer,CustomerSupporterSerializer,DriverSerializer,SupplierSerializer
from .models import Admin,CustomerSupporter,Driver,Supplier,Customer
from rest_framework.views import APIView


class CustomerList(APIView):
    
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        #here need to make sure that who is deleting is an admin
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminList(APIView):
    
    def post(self, request, format=None):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDetail(APIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get_object(self, pk):
        try:
            return Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        admin = self.get_object(pk)
        serializer = AdminSerializer(admin)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        admin = self.get_object(pk)
        #here need to update condition in case admin is content manager
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SupplierList(APIView):
    
    def post(self, request, format=None):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierDetail(APIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        supplier = self.get_object(pk)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        supplier = self.get_object(pk)
        #here need to update
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverList(APIView):
    
    def post(self, request, format=None):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverDetail(APIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_object(self, pk):
        try:
            return Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        driver = self.get_object(pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        driver = self.get_object(pk)
        #here need to update
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerSupporterList(APIView):
    
    def post(self, request, format=None):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerSupporterDetail(APIView):
    queryset = CustomerSupporter.objects.all()
    serializer_class = CustomerSupporterSerializer

    def get_object(self, pk):
        try:
            return CustomerSupporter.objects.get(pk=pk)
        except CustomerSupporter.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer_supporter = self.get_object(pk)
        serializer = CustomerSupporterSerializer(customer_supporter)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        customer_supporter = self.get_object(pk)
        #here need to update
        customer_supporter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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


