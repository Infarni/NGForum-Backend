from rest_framework import serializers
from .models import UserModel
from posts.serializers import *


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    username = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    discription = serializers.CharField(
        max_length=1024,
        required=False
    )
    avatar = serializers.ImageField(required=False)
    posts = serializers.StringRelatedField(many=True, read_only=True)
    
    
    def create(self, validated_data):
        instance = UserModel.objects.create(**validated_data)
        instance.set_password(validated_data['password'])

        instance.save()
        
        return instance
    
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.discription = validated_data.get('discription', instance.discription)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        
        instance.save()
        
        return instance
