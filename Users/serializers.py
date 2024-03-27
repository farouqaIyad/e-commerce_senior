from rest_framework import serializers
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.password_validation import validate_password 

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        pass 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        pass 

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        pass          

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        pass  

class CustomerSupporterSerializer(serializers.ModelSerializer):
    class Meta:
        pass    