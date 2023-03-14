from rest_framework import serializers
from users.models import UserModel
from .models import *


class PostRatingSerializer(serializers.Serializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    
    def create(self, validated_data):
        return PostRatingModel.objects.create(**validated_data)


class PostImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=True)
    
    
    def create(self, validated_data):
        return PostImageModel.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.post = validated_data.get('post', instance.post)
        instance.image = validated_data.get('image', instance.image)
        
        instance.save()
        
        return instance



class PostCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    body = serializers.CharField(max_length=1024)
    
    
    def create(self, validated_data):
        return PostCommentModel.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        
        instance.save()
        
        return instance


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(max_length=256)
    body = serializers.CharField(max_length=4096)
    date_create = serializers.DateTimeField(read_only=True)
    date_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField()
    rating = serializers.IntegerField(read_only=True)
    num_comments = serializers.IntegerField(read_only=True)
    
    
    def create(self, validated_data):
        return PostModel.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.is_published = validated_data.get('is_published', instance.is_published)

        instance.save()
        
        return instance
