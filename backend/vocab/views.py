from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Card, Word
from .serializers import CardSerializer, ReviewSerializer
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
            new_words = Word.objects.exclude(cards__user=request.user)[:missing]
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
