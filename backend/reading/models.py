"""Reading (T1.4, T1.5): bài đọc, nhóm câu hỏi, câu hỏi, lượt làm bài.

Cấu trúc giống đề IELTS thật: mỗi bài đọc có nhiều nhóm câu hỏi ("Questions 1-5"),
mỗi nhóm một dạng và một lời dặn chung; dạng Matching dùng chung một danh sách lựa chọn.
Đáp án lưu dạng danh sách các cách viết được chấp nhận (JSON) để dùng lại cho Listening.
"""
from django.conf import settings
from django.db import models


class Passage(models.Model):
    class Module(models.TextChoices):
        ACADEMIC = "academic", "Academic"
        GENERAL = "general", "General Training"

    title = models.CharField(max_length=200, unique=True)
    topic = models.CharField(max_length=60)
    module = models.CharField(max_length=10, choices=Module.choices, default=Module.ACADEMIC)
    difficulty = models.PositiveSmallIntegerField(default=2)  # 1 dễ, 2 vừa, 3 khó
    minutes = models.PositiveSmallIntegerField(default=20)
    body = models.TextField(help_text="Các đoạn cách nhau một dòng trống; đoạn được gắn nhãn A, B, C...")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class QuestionGroup(models.Model):
    class Kind(models.TextChoices):
        MCQ = "mcq", "Multiple choice"
        TFNG = "tfng", "True / False / Not Given"
        YNNG = "ynng", "Yes / No / Not Given"
        HEADINGS = "headings", "Matching headings"
        MATCH_INFO = "match_info", "Matching information"
        COMPLETION = "completion", "Sentence completion"

    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name="groups")
    order = models.PositiveSmallIntegerField(default=1)
    kind = models.CharField(max_length=12, choices=Kind.choices)
    instructions = models.TextField()
    # Matching: [{"key": "i", "text": "..."}]; các dạng khác để trống
    options = models.JSONField(default=list, blank=True)
    max_words = models.PositiveSmallIntegerField(null=True, blank=True)  # Completion: "NO MORE THAN TWO WORDS"

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.passage} - {self.get_kind_display()}"


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name="questions")
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
    choices = models.JSONField(default=list, blank=True)  # MCQ: [{"key": "A", "text": "..."}]
    answers = models.JSONField(help_text='Các đáp án được chấp nhận, ví dụ ["TRUE"] hoặc ["varroa mite", "varroa"]')
    explanation = models.TextField(blank=True)
    evidence = models.TextField(blank=True, help_text="Đoạn trích nguyên văn trong bài đọc chứa đáp án")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Q{self.number}"


class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_attempts")
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name="attempts")
    answers = models.JSONField(default=dict)   # {"1": "TRUE", "10": "wild bees"}
    results = models.JSONField(default=list)   # kết quả từng câu (xem grading.grade)
    correct = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    band = models.FloatField(default=0)
    duration_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.passage} ({self.correct}/{self.total})"
