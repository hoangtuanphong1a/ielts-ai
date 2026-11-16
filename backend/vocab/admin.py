from django.contrib import admin

from .models import Card, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["term", "topic"]
    search_fields = ["term"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "repetitions", "interval", "ease", "due_date"]
