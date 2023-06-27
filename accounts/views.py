from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import UserModel
from .serializers import UserSerializer
from .permissions import IsOwnUserOrReadOnly, IsNotAuthenticated


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', '')
        queryset = UserModel.objects.filter(username__icontains=username)
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsNotAuthenticated()]
        
        return [IsOwnUserOrReadOnly()]
    
    def get_parsers(self):
        return [JSONParser(), MultiPartParser()]
