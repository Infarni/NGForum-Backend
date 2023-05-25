from django.urls import path
from .views import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/verify', TokenVerifyView.as_view(), name='token_verify'),
]
