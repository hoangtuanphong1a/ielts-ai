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
        fields = ["id", "word", "repetitions", "interval", "ease", "due_date", "context", "source"]


class ReviewSerializer(serializers.Serializer):
    quality = serializers.IntegerField(min_value=0, max_value=5)


class LookupQuerySerializer(serializers.Serializer):
    word = serializers.CharField(max_length=40)
    context = serializers.CharField(max_length=400, required=False, allow_blank=True, default="")


class AddCardSerializer(serializers.Serializer):
    term = serializers.CharField(max_length=100)
    definition = serializers.CharField(max_length=500)
    context = serializers.CharField(max_length=400, required=False, allow_blank=True, default="")
    source = serializers.CharField(max_length=200, required=False, allow_blank=True, default="")
