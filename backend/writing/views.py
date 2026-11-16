from django.conf import settings
from django.db.models import Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml.scorer import score_essay

from .models import Submission, WritingPrompt
from .serializers import SubmissionSerializer, WritingPromptSerializer


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
        prompt = serializer.validated_data["prompt"]
        essay = serializer.validated_data["essay"]

        result = score_essay(
            essay,
            prompt=prompt.prompt_text,
            task_type=prompt.task_type,
            model_path=settings.ML_MODEL_PATH,
        )

        serializer.save(
            user=self.request.user,
            word_count=int(result.features["word_count"]),
            band_overall=result.overall,
            band_task_response=result.task_response,
            band_coherence=result.coherence,
            band_lexical=result.lexical,
            band_grammar=result.grammar,
            feedback=result.feedback,
            features=result.features,
            scorer=result.scorer,
        )


@extend_schema(responses=OpenApiTypes.OBJECT, description="Lịch sử band + trung bình 4 tiêu chí của user hiện tại")
@api_view(["GET"])
def progress(request):
    qs = Submission.objects.filter(user=request.user)
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
