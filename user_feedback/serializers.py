from rest_framework import serializers
from .models import Review,Complaints
from catalog.models import Product
from Users.models import User
from django.db import models


class ReviewSerializer(serializers.Serializer):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)

    def create(self,validated_data):
        validated_data['product'] = self.context.get('product')
        validated_data['customer'] = self.context.get('customer')
        return super().create(validated_data)

    class Meta:
        db_table = 'review'
        fields = ['rating', 'comment'
                  ]

class ComplaintsSerializer(serializers.Serializer):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    #order = models.ForeignKey(Order,on_delete = models.CASCADE)

    def create(self,validated_data):
        validated_data['customer'] = self.context.get('customer')
        validated_data['order'] = self.context.get('order')

        return super().create(validated_data)
    class Meta:
        db_table = 'complaints'
        fields = ['order', 'complain_type', 'status_type']


