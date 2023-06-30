from django.db import models
from django.conf import settings


def user_directory_path_post_images(instance, filename):
    username = instance.question.owner.username
    id = instance.question.id
    return f'users/{username}/question/{id}/images/{filename}'


class QuestionAssessmentManager(models.Manager):
    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)

        if not obj.value:
            obj.question.rating -= 1
        else:
            obj.question.rating += 1

        obj.question.save()

        return obj


class AnswerAssessmentManager(models.Manager):
    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)

        if not obj.value:
            obj.answer.rating -= 1
        else:
            obj.answer.rating += 1

        obj.answer.save()

        return obj


class TagModel(models.Model):
    name = models.CharField(max_length=32, blank=False)


class QuestionModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='questions',
        on_delete=models.CASCADE,
        editable=False,
        blank=False,
    )
    tag = models.ForeignKey(
        TagModel,
        related_name='questions',
        on_delete=models.CASCADE,
        editable=False,
        blank=False,
    )
    title = models.CharField(max_length=512, blank=False)
    body = models.TextField(max_length=8192, blank=False)
    rating = models.IntegerField(default=0)


class ImageModel(models.Model):
    question = models.ForeignKey(
        QuestionModel,
        related_name='images',
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    image = models.ImageField(upload_to=user_directory_path_post_images)


class QuestionAssessmentModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    question = models.ForeignKey(
        QuestionModel,
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    value = models.BooleanField()

    objects = QuestionAssessmentManager()

    def delete(self, using=None, keep_parents=False):
        if not self.value:
            self.question.rating += 1

        self.question.rating -= 1

        self.question.save()

        super().delete(using, keep_parents)


class AnswerModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='answers',
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    question = models.ForeignKey(
        QuestionModel,
        related_name='answers',
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    body = models.TextField(max_length=8192, blank=False)
    rating = models.IntegerField(default=0)


class AnswerAssessmentModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    answer = models.ForeignKey(
        AnswerModel,
        on_delete=models.CASCADE,
        editable=False,
        blank=False
    )
    value = models.BooleanField()

    objects = AnswerAssessmentManager()

    def delete(self, using=None, keep_parents=False):
        if not self.value:
            self.answer.rating += 1

        self.answer.rating -= 1

        self.answer.save()

        super().delete(using, keep_parents)
