from django.apps import AppConfig


class CoachConfig(AppConfig):
    """Bộ máy cá nhân hoá: điểm yếu, kế hoạch hôm nay, đề xuất đề (Phase 3)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "coach"
