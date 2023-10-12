from rest_framework import serializers
from .models import *

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class managerSerializer(serializers.ModelSerializer):
    class Meta:
        model = manager
        fields = '__all__'
