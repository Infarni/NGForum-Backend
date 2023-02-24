from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from users.views import *
from posts.views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'images', PostImageViewSet, basename='images')
router.register(r'comments', PostCommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
