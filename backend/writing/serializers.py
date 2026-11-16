from rest_framework import serializers

from .models import Submission, WritingPrompt


class WritingPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingPrompt
        fields = ["id", "task_type", "title", "prompt_text"]


class SubmissionSerializer(serializers.ModelSerializer):
    prompt_title = serializers.CharField(source="prompt.title", read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id", "prompt", "prompt_title", "essay", "word_count",
            "band_overall", "band_task_response", "band_coherence",
            "band_lexical", "band_grammar", "feedback", "features",
            "scorer", "status", "error", "issues", "created_at",
        ]
        read_only_fields = [
            "word_count", "band_overall", "band_task_response", "band_coherence",
            "band_lexical", "band_grammar", "feedback", "features",
            "scorer", "status", "error", "issues", "created_at",
        ]

    def validate_essay(self, value):
        if len(value.split()) < 20:
            raise serializers.ValidationError("Your essay is too short (at least 20 words).")
        return value
