from django.db import models
from django.utils import timezone
from django.conf import settings


def user_directory_path_post_images(instance, filename):
    username = instance.post.author.username
    id = instance.post.id
    return f'users/{username}/posts/{id}/images/{filename}'


class PostModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=256)
    body = models.TextField(max_length=4096, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = 'Публікація'
        verbose_name_plural = 'Публікації'


    def __str__(self):
        return self.title
    

class PostImageModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to=user_directory_path_post_images)
    
    
    class Meta:
        verbose_name = 'Зображення'
        verbose_name_plural = 'Зображення'


    def __str__(self):
        return self.post


class PostCommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    body = models.TextField(max_length=1024)


    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'


    def __str__(self):
        return self.author
