from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import *
from posts.views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'images', PostImageViewSet, basename='images')
router.register(r'comments', PostCommentViewSet, basename='comments')

schema_view = get_schema_view(
   openapi.Info(
      title='NGForum API',
      default_version='v1',
      description='Test description',
      contact=openapi.Contact(email='archdroider@proton.me'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
