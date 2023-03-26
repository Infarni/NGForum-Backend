from rest_framework import serializers

from .models import UserModel


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=64, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    discription = serializers.CharField(max_length=1024, required=False)
    avatar = serializers.ImageField(required=False)
    

    def create(self, validated_data):
            password = validated_data.pop('password')

            instance = UserModel.objects.create(**validated_data)
            instance.set_password(password)

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
