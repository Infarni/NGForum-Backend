from django.contrib import admin
from .models import PostModel, PostImageModel, PostCommentModel


admin.site.register(PostModel)
admin.site.register(PostImageModel)
admin.site.register(PostCommentModel)

