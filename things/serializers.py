from rest_framework import serializers
from .models import Thing
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class ThingsSerializer(serializers.ModelSerializer):
    # owner_name = UserSerializer(read_only=True)
    owner_name = serializers.CharField(source='owner', read_only=True)

    class Meta:
        model = Thing
        fields = '__all__'
