from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from accounts.views import AccountViewSet
from forum.views import (
    TagViewSet,
    QuestionViewSet,
    AnswerViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
