from rest_framework import viewsets

from .models import UserModel
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer