from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.models import UserModel

from .models import PostModel, PostImageModel, PostCommentModel
from .serializers import *


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

    def get_queryset(self):
        author_id = self.request.data.get('author')
        if not author_id:
            return PostModel.objects.all()

        author = UserModel.objects.get(id=self.request.data['author'])
        
        queryset = PostModel.objects.filter(author=author)
        
        return queryset


class PostImageViewSet(viewsets.ModelViewSet):
    serializer_class = PostImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = PostModel.objects.get(id=post_id)
        
        serializer.save(post=post)
    
    
    def get_queryset(self):
        post_id = self.request.data.get('post')
        if not post_id:
            return PostImageModel.objects.all()

        post = PostModel.objects.get(id=post_id)
        
        queryset = PostImageModel.objects.filter(post=post)
        
        return queryset


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = PostModel.objects.get(id=post_id)
        
        serializer.save(author=self.request.user, post=post)
    
    
    def get_queryset(self):
        post_id = self.request.data.get('post')
        if not post_id:
            return PostCommentModel.objects.all()

        post = PostModel.objects.get(id=post_id)
        
        queryset = PostCommentModel.objects.filter(post=post)
        
        return queryset
