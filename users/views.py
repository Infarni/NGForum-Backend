from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserModel
from posts.models import PostModel
from posts.serializers import PostSerializer
from .serializers import *
from .permissions import IsOwnUserOrReadOnly, IsNotAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnUserOrReadOnly,)


    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = PostModel.objects.filter(author=user)
        
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data)
