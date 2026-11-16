from datetime import timedelta

from django.utils import timezone
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from ml.dictionary import lookup as dictionary_lookup

from .models import Card, Word
from .serializers import AddCardSerializer, CardSerializer, LookupQuerySerializer, ReviewSerializer
from .srs import sm2

DAILY_TARGET = 10


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.none()  # cho Swagger biết kiểu id; dữ liệu thật lọc ở get_queryset

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).select_related("word")

    @action(detail=False, methods=["get"])
    def due(self, request):
        today = timezone.localdate()
        due = list(self.get_queryset().filter(due_date__lte=today)[:DAILY_TARGET])

        # Chưa đủ thẻ đến hạn -> thêm từ mới user chưa học
        missing = DAILY_TARGET - len(due)
        if missing > 0:
            new_words = Word.objects.filter(added_by__isnull=True).exclude(cards__user=request.user)[:missing]
            due += [Card.objects.create(user=request.user, word=w) for w in new_words]

        return Response(CardSerializer(due, many=True).data)

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        card = self.get_object()
        ser = ReviewSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        card.repetitions, card.interval, card.ease = sm2(
            ser.validated_data["quality"], card.repetitions, card.interval, card.ease
        )
        card.due_date = timezone.localdate() + timedelta(days=card.interval)
        card.last_reviewed = timezone.now()
        card.save()
        return Response(CardSerializer(card).data)

    @extend_schema(request=AddCardSerializer, responses=CardSerializer)
    @action(detail=False, methods=["post"])
    def add(self, request):
        """REA-04: lưu từ vừa tra vào bộ thẻ của học viên (đến hạn ôn ngay hôm nay)."""
        ser = AddCardSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        term = data["term"].strip().lower()
        word = Word.objects.filter(term__iexact=term).first() or Word.objects.create(
            term=term, definition=data["definition"], example=data["context"], topic="reading",
            added_by=request.user,
        )
        card, created = Card.objects.get_or_create(
            user=request.user, word=word, defaults={"context": data["context"], "source": data["source"]},
        )
        return Response(CardSerializer(card).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@extend_schema(parameters=[LookupQuerySerializer], responses=OpenApiTypes.OBJECT,
               summary="Look up a word offline (WordNet), ranked by the sentence it appears in")
@api_view(["GET"])
def lookup(request):
    query = LookupQuerySerializer(data=request.query_params)
    query.is_valid(raise_exception=True)
    result = dictionary_lookup(query.validated_data["word"], query.validated_data["context"])
    if result is None:
        return Response({"detail": "No definition found."}, status=status.HTTP_404_NOT_FOUND)
    result["in_deck"] = Card.objects.filter(user=request.user, word__term__iexact=result["lemma"]).exists()
    return Response(result)
