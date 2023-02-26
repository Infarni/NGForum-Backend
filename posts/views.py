from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import UserModel
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PostModel, PostImageModel, PostCommentModel, PostRatingModel
from .serializers import *
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.order_by('-date_update')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(detail=True, methods=['get', 'post', 'delete'])
    def rate(self, request, pk=None):
        user = request.user
        post = self.get_object()
        rating = PostRatingModel.objects.filter(author=user, post=post)
        
        if request.method == 'GET':
            if rating.exists():
                return Response({'detail': 'Вподобайка вже існує.'})
            return Response(
                {'detail': 'Вподобайка не знайдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
   
        if request.method == 'DELETE':
            if rating.exists():
                rating = PostRatingModel.objects.get(author=user, post=post)
                rating.delete()
                
                post.rating -= 1
                post.save()
    
                return Response({'detail': 'Вподобайка успішно видалена.'})
                
            return Response(
                {'detail': 'Вподобайка не знайдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if rating.exists():
            return Response({'detail': 'Вподобайка вже існує.'})

        rating_serializer = PostRatingSerializer(data={'author': user, 'post': post})
        rating_serializer.is_valid(raise_exception=True)
        rating_serializer.save(author=user, post=post)

        post.rating += 1
        post.save()
        
        return Response(rating_serializer.data)
    
    
    @action(detail=True, methods=['get', 'post', 'delete'])
    def comments(self, request, pk=None):
        user = request.user
        post = self.get_object()
        
        if request.method == 'GET':
            queryset = PostCommentModel.objects.filter(post=post)
            serializer = PostCommentSerializer(queryset, many=True)
            
            return Response(serializer.data)
        
        data = {'post': post, 'author': user, 'body': request.data.get('body')}
        
        serializer = PostCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=user)
        
        post.num_comments += 1
        post.save()
            
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post', 'delete'],)
    def images(self, request, pk=None):
        user = request.user
        post = self.get_object()
        
        if request.method == 'GET':
            queryset = PostImageModel.objects.filter(post=post)
            serializer = PostImageSerializer(queryset, many=True)
            
            return Response(serializer.data)
        
        data = {'post': post, 'author': user, 'image': request.data.get('image')}
        
        serializer = PostImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        
        return Response(serializer.data)


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImageModel.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = PostModel.objects.get(id=post_id)
        
        serializer.save(post=post)


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostCommentModel.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = PostModel.objects.get(id=post_id)
        
        serializer.save(author=self.request.user, post=post)
