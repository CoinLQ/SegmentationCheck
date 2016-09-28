from django.contrib import admin

# Register your models here.
from .models import QuizBatch, QuizResult

admin.site.register(QuizBatch)
admin.site.register(QuizResult)
