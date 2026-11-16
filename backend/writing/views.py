from django.db import transaction
from django.db.models import Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Submission, WritingPrompt
from .serializers import SubmissionSerializer, WritingPromptSerializer
from .tasks import score_submission


class WritingPromptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WritingPrompt.objects.all().order_by("id")
    serializer_class = WritingPromptSerializer


class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.none()  # cho Swagger biết kiểu id; dữ liệu thật lọc ở get_queryset

    def get_queryset(self):
        # Mỗi user chỉ thấy bài của mình
        return Submission.objects.filter(user=self.request.user).select_related("prompt")

    def perform_create(self, serializer):
        # T2.1: lưu bài ở trạng thái pending, trả lời ngay; chấm ở nền.
        # on_commit: chỉ xếp task sau khi bài đã nằm trong DB (worker đọc được).
        sub = serializer.save(user=self.request.user, status=Submission.Status.PENDING)
        transaction.on_commit(lambda: score_submission.delay(sub.pk))


@extend_schema(responses=OpenApiTypes.OBJECT, description="Band history and averages of the 4 criteria for the current user")
@api_view(["GET"])
def progress(request):
    # Chỉ tính bài đã chấm xong (T2.1)
    qs = Submission.objects.filter(user=request.user, status=Submission.Status.DONE)
    history = [
        {"id": s.id, "date": s.created_at.date().isoformat(), "band": s.band_overall}
        for s in qs.order_by("created_at")
    ]
    averages = qs.aggregate(
        overall=Avg("band_overall"),
        task_response=Avg("band_task_response"),
        coherence=Avg("band_coherence"),
        lexical=Avg("band_lexical"),
        grammar=Avg("band_grammar"),
    )
    return Response({"count": qs.count(), "history": history, "averages": averages})
