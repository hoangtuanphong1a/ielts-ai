from django.conf import settings
from django.db import models
from django.utils import timezone


class Word(models.Model):
    term = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    example = models.TextField(blank=True)
    topic = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.term


class Card(models.Model):
    """Thẻ flashcard của 1 user cho 1 từ, lưu trạng thái SM-2."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="cards")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="cards")
    repetitions = models.PositiveIntegerField(default=0)
    interval = models.PositiveIntegerField(default=0)  # số ngày
    ease = models.FloatField(default=2.5)
    due_date = models.DateField(default=timezone.localdate)
    last_reviewed = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("user", "word")]
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.user} - {self.word} (due {self.due_date})"
