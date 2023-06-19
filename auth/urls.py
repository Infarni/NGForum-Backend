from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('/verify', TokenVerifyView.as_view(), name='token_verify'),
]
