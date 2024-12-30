from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LostFoundItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = { 'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LostFoundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostFoundItem
        fields = ['id', 'user', 'title', 'description', 'image', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
        extra_kwargs = {
            'description': {'required': False},
            'image': {'required': False}, 
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)