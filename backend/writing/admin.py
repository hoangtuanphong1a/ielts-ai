from django.contrib import admin

from .models import Submission, WritingPrompt


@admin.register(WritingPrompt)
class WritingPromptAdmin(admin.ModelAdmin):
    list_display = ["id", "task_type", "title"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "prompt", "band_overall", "scorer", "created_at"]
    list_filter = ["scorer"]
