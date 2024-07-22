from rest_framework import serializers
from .models import notification


class notificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = notification
        fields = "__all__"
