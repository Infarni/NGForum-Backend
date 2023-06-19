from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth.serializers import CustomTokenObtainPairSerializer, CustonTokenRefreshSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustonTokenRefreshSerializer
