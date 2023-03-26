from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import (
    TagModel,
    QuestionModel,
    ImageModel,
    AnswerModel,
    QuestionAssessmentModel,
    AnswerAssessmentModel
)


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(read_only=True)


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = UserSerializer(read_only=True)
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionModel.objects.all(),
        required=True
    )
    body = serializers.CharField(max_length=8192, required=True)
    rating = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = self.context['user']

        instance = AnswerModel.objects.create(owner=user, **validated_data)

        return instance

    def update(self, instance, validated_data):
        body = validated_data.get('body', instance.body)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = UserSerializer(read_only=True)
    tag = serializers.PrimaryKeyRelatedField(
        queryset=TagModel.objects.all(),
        required=True
    )
    title = serializers.CharField(max_length=512, required=True)
    body = serializers.CharField(max_length=8192, required=True)
    rating = serializers.IntegerField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    answers = AnswerSerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = self.context['user']

        images = []
        if 'uploaded_images' in validated_data:
            images = validated_data.pop('uploaded_images')

        instance = QuestionModel.objects.create(owner=user, **validated_data)

        for image in images:
            ImageModel.objects.create(question=instance, image=image)

        return instance

    def update(self, instance, validated_data):
        instance.tag = validated_data.get('tag', instance.tag)
        instance.title = validated_data.get('title', instance.title)
        body = validated_data.get('body', instance.body)



class QuestionPreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = UserSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=32, required=True)
    questions = QuestionPreviewSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return TagModel.objects.create(**validated_data)


class QuestionAssessmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True),
    owner = UserSerializer(read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    value = serializers.BooleanField()
    
    
    def create(self, validated_data):
        user = self.context['user']
        question = self.context['questions']
        
        instance = QuestionAssessmentModel.objects.create(
            owner=user,
            question=question,
            **validated_data
        )
        
        return instance
    
    
    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        
        instance.save()
        
        return instance


class AnswerAssessmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True),
    owner = UserSerializer(read_only=True)
    answer = serializers.PrimaryKeyRelatedField(read_only=True)
    value = serializers.BooleanField()
    
    
    def create(self, validated_data):
        user = self.context['user']
        answer = self.context['answer']
        
        instance = AnswerAssessmentModel.objects.create(
            owner=user,
            answer=answer,
            **validated_data
        )
        
        return instance
    
    
    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        
        instance.save()
        
        return instance
