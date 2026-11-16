from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "target_band", "exam_date", "daily_minutes"]
    list_filter = ["role"]
    search_fields = ["user__username", "user__email"]
