from django.db.models import Count, Max, Prefetch, Q
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .grading import grade
from .models import Attempt, Passage, QuestionGroup
from .serializers import AttemptCreateSerializer, AttemptSerializer, PassageDetailSerializer, PassageListSerializer

GROUPS = Prefetch("groups", queryset=QuestionGroup.objects.prefetch_related("questions"))


class PassageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Passage.objects.none()

    def get_queryset(self):
        if self.action == "list":
            mine = Q(attempts__user=self.request.user)
            return Passage.objects.annotate(
                question_count=Count("groups__questions", distinct=True),
                best_band=Max("attempts__band", filter=mine),
                attempt_count=Count("attempts", filter=mine, distinct=True),
            ).order_by("id")
        return Passage.objects.prefetch_related(GROUPS)

    def get_serializer_class(self):
        return PassageListSerializer if self.action == "list" else PassageDetailSerializer

    @extend_schema(request=AttemptCreateSerializer, responses=AttemptSerializer)
    @action(detail=True, methods=["post"])
    def attempts(self, request, pk=None):
        """Nộp bài: chấm ngay (nhẹ, không cần Celery) và trả kết quả từng câu."""
        passage = self.get_object()
        data = AttemptCreateSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        result = grade(passage, data.validated_data["answers"])
        attempt = Attempt.objects.create(
            user=request.user, passage=passage, answers=data.validated_data["answers"],
            duration_seconds=data.validated_data["duration_seconds"], **result,
        )
        return Response(AttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


class AttemptViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AttemptSerializer
    queryset = Attempt.objects.none()

    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user).select_related("passage").prefetch_related(
            Prefetch("passage__groups", queryset=QuestionGroup.objects.prefetch_related("questions")))
