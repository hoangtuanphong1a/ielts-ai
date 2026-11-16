from django.conf import settings
from django.db import models


class WritingPrompt(models.Model):
    TASK_CHOICES = [("task1", "Task 1"), ("task2", "Task 2")]

    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, default="task2")
    title = models.CharField(max_length=200)
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.task_type}] {self.title}"


class Submission(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SCORING = "scoring", "Scoring"
        DONE = "done", "Done"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="submissions")
    prompt = models.ForeignKey(WritingPrompt, on_delete=models.CASCADE,
                               related_name="submissions")
    essay = models.TextField()
    word_count = models.PositiveIntegerField(default=0)

    band_overall = models.FloatField(default=0)
    band_task_response = models.FloatField(default=0)
    band_coherence = models.FloatField(default=0)
    band_lexical = models.FloatField(default=0)
    band_grammar = models.FloatField(default=0)

    feedback = models.JSONField(default=list)
    features = models.JSONField(default=dict)
    issues = models.JSONField(default=list, blank=True)  # T2.3: lỗi ngữ pháp/chính tả (LanguageTool)
    scorer = models.CharField(max_length=20, default="heuristic")
    # T2.1: chấm ở nền. Bài cũ (đã chấm đồng bộ) mặc định là done.
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DONE, db_index=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.prompt.title} - {self.band_overall}"
