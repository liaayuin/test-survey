from django.contrib import admin
from .models import (
    Respondent,
    QuestionCategory,
    MultiSelectOption,
    MultiSelectAnswer
)

admin.site.register(Respondent)
admin.site.register(QuestionCategory)
admin.site.register(MultiSelectOption)
admin.site.register(MultiSelectAnswer)