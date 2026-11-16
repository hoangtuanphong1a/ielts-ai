from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Role(models.TextChoices):
    STUDENT = "student", "Student"
    TEACHER = "teacher", "Teacher"
    ADMIN = "admin", "Admin"


class Profile(models.Model):
    """Hồ sơ 1-1 với User: vai trò + mục tiêu học (AUTH-09, AUTH-10)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profile")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    target_band = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(4.0), MaxValueValidator(9.0)],
    )
    exam_date = models.DateField(null=True, blank=True)
    daily_minutes = models.PositiveSmallIntegerField(
        default=30, validators=[MinValueValidator(10), MaxValueValidator(300)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} ({self.role})"
