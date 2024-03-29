from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from accounts.models import UserModel

from .models import (
    TagModel,
    QuestionModel,
    AnswerModel,
    QuestionAssessmentModel,
    AnswerAssessmentModel,
)

from .serializers import (
    TagSerializer,
    QuestionSerializer,
    AnswerSerializer,
    QuestionAssessmentSerializer,
    AnswerAssessmentSerializer
)

from .permissions import IsOwnUserOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        queryset = TagModel.objects.filter(name__icontains=name)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        return [IsOwnUserOrReadOnly()]


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def get_queryset(self):
        return QuestionModel.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        return [IsOwnUserOrReadOnly()]

    def create(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        methods=['get'],
        responses={
            200: None,
            404: None
        }
    )
    @extend_schema(
        methods=['post'],
        request=AnswerAssessmentSerializer,
        responses={
            200: None,
            201: None
        }
    )
    @extend_schema(
        methods=['delete'],
        responses={
            204: None,
            404: None
        }
    )
    @action(detail=True, methods=['get', 'post', 'delete'])
    def assessment(self, request, pk=None):
        question = self.get_object()
        owner = request.user
        
        try:
            assessment = QuestionAssessmentModel.objects.get(
                question=question,
                owner=owner
            )
        except ObjectDoesNotExist:
            assessment = None
        if request.method == 'DELETE':
            if assessment:
                assessment.delete()
                
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if assessment:
            return Response()
        
        if request.method == 'POST':
            serializer = QuestionAssessmentSerializer(
                data=request.data,
                context={'question': question, 'user': owner}
            )
            serializer.is_valid(raise_exception=True)
            
            serializer.save()
            
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnswerViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser]

    def get_queryset(self):
        return AnswerModel.objects.all()
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        
        return [IsOwnUserOrReadOnly()]
    
    def get_serializer_class(self):
        if self.action == 'assessment':
            return AnswerAssessmentSerializer
        
        return AnswerSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        methods=['get'],
        responses={
            200: None,
            404: None
        }
    )
    @extend_schema(
        methods=['post'],
        request=AnswerAssessmentSerializer,
        responses={
            200: None,
            201: None
        }
    )
    @extend_schema(
        methods=['delete'],
        responses={
            204: None,
            404: None
        }
    )
    @action(detail=True, methods=['get', 'post', 'delete'])
    def assessment(self, request, pk=None):
        answer = self.get_object()
        owner = request.user
        
        try:
            assessment = AnswerAssessmentModel.objects.get(
                answer=answer,
                owner=owner
            )
        except ObjectDoesNotExist:
            assessment = None
        if request.method == 'DELETE':
            if assessment:
                assessment.delete()
                
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if assessment:
            return Response()
        
        if request.method == 'POST':
            serializer = AnswerAssessmentSerializer(
                data=request.data,
                context={'answer': answer, 'user': owner}
            )
            serializer.is_valid(raise_exception=True)
            
            serializer.save()
            
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
