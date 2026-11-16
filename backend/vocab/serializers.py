from rest_framework import serializers

from .models import Card, Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "term", "definition", "example", "topic"]


class CardSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = Card
        fields = ["id", "word", "repetitions", "interval", "ease", "due_date"]


class ReviewSerializer(serializers.Serializer):
    quality = serializers.IntegerField(min_value=0, max_value=5)
