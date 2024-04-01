from rest_framework import serializers
from .models import Review,Complaints

class ReviewSerializer(serializers.Serializer):
    class Meta:
        db_table = 'review'
        fields = ['rating', 'comment', 'product']

class ComplaintsSerializer(serializers.Serializer):
    class Meta:
        db_table = 'complains'
        fields = ['order', 'complain_type', 'status_type']


