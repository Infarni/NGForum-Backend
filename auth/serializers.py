from accounts.models import UserModel

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.backends import TokenBackend

from accounts.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        serializer = UserSerializer(user)
        data['user'] = serializer.data

        return data


class CustonTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = attrs['refresh']
        token_backend = TokenBackend(algorithm='HS256')
        token = token_backend.decode(refresh, verify=False)
        user_id = token['user_id']

        user = UserModel.objects.get(id=user_id)

        serializer = UserSerializer(user)
        data['user'] = serializer.data

        return data
