from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth.hashers import make_password 
from rest_framework import serializers
from .models import User,Address
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

class AddressSerializer(serializers.ModelSerializer):
    customer = models.ForeignKey(User,on_delete = models.CASCADE)
    
    def create(self,validated_data):
        validated_data['customer'] = self.context.get('customer')
        return super().create(validated_data)

    class Meta:
        model = Address
        fields = ['address_name','city','district','details','phone_number']

    

    