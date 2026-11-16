from rest_framework import serializers

from .models import Attempt, Passage, Question, QuestionGroup


class QuestionSerializer(serializers.ModelSerializer):
    """Không gửi đáp án / giải thích khi đang làm bài."""

    class Meta:
        model = Question
        fields = ["number", "text", "choices"]


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionGroup
        fields = ["id", "kind", "instructions", "options", "max_words", "questions"]


class PassageListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    best_band = serializers.FloatField(read_only=True, allow_null=True)
    attempt_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Passage
        fields = ["id", "title", "topic", "module", "difficulty", "minutes", "question_count", "best_band", "attempt_count"]


class PassageDetailSerializer(serializers.ModelSerializer):
    groups = QuestionGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Passage
        fields = ["id", "title", "topic", "module", "difficulty", "minutes", "body", "groups"]


class AttemptCreateSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.CharField(allow_blank=True, max_length=100), allow_empty=True)
    duration_seconds = serializers.IntegerField(min_value=0, max_value=4 * 3600, default=0)


class AttemptSerializer(serializers.ModelSerializer):
    passage = PassageDetailSerializer(read_only=True)

    class Meta:
        model = Attempt
        fields = ["id", "passage", "answers", "results", "correct", "total", "band", "duration_seconds", "created_at"]
