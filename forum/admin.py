from django.contrib import admin

from .models import (
    TagModel,
    QuestionModel,
    ImageModel,
    QuestionAssessmentModel,
    AnswerAssessmentModel
)


admin.site.register(TagModel)
admin.site.register(QuestionModel)
admin.site.register(ImageModel)
admin.site.register(QuestionAssessmentModel)
admin.site.register(AnswerAssessmentModel)
