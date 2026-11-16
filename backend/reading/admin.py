from django.contrib import admin

from .models import Attempt, Passage, Question, QuestionGroup


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ["passage", "order", "kind"]
    inlines = [QuestionInline]


class GroupInline(admin.StackedInline):
    model = QuestionGroup
    extra = 0
    show_change_link = True


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "module", "difficulty", "minutes"]
    inlines = [GroupInline]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "passage", "correct", "total", "band", "created_at"]
    list_filter = ["passage"]
