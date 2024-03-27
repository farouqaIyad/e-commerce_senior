from rest_framework import serializers
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.password_validation import validate_password 
from .models import Admin,Supplier,Customer,Driver,CustomerSupporter

class AdminSerializer(serializers.ModelSerializer):
    
    def validate_password(self, value):
        validate_password(value)  
        return make_password(value)  

    class Meta:
        model = Admin
        fields = '__all__'  

    def create(self, validated_data):
        validated_data['password'] = self.validate_password(validated_data['password'])
        return super().create(validated_data)

class SupplierSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        validate_password(value)  
        return make_password(value)  

    class Meta:
        model = Supplier
        fields = '__all__'  

    def create(self, validated_data):
        validated_data['password'] = self.validate_password(validated_data['password'])
        return super().create(validated_data) 

class CustomerSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)  
        return make_password(value)  

    class Meta:
        model = Customer
        fields = '__all__'  

    def create(self, validated_data):
        validated_data['password'] = self.validate_password(validated_data['password'])
        return super().create(validated_data)         

class DriverSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)  
        return make_password(value)  

    class Meta:
        model = Driver
        fields = '__all__'  

    def create(self, validated_data):
        validated_data['password'] = self.validate_password(validated_data['password'])
        return super().create(validated_data) 

class CustomerSupporterSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)  
        return make_password(value)  

    class Meta:
        model = CustomerSupporter
        fields = '__all__'  

    def create(self, validated_data):
        validated_data['password'] = self.validate_password(validated_data['password'])
        return super().create(validated_data)   