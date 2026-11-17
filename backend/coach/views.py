from django.utils import timezone
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reading.models import Attempt
from writing.models import Submission

from .plan import build_today
from .week import build_week
from .weakness import READING_RECENT, RECENT, detect_weaknesses


@extend_schema(responses=OpenApiTypes.OBJECT, summary="Top weaknesses and today's personalised plan")
@api_view(["GET"])
def today(request):
    """T3.3 + T3.4 + T3.5: điểm yếu có số liệu, kế hoạch hôm nay theo số phút, đề đề xuất."""
    subs = list(
        Submission.objects.filter(user=request.user, status=Submission.Status.DONE)
        .select_related("prompt").order_by("-created_at")[:RECENT]
    )
    profile = getattr(request.user, "profile", None)
    target = profile.target_band if profile else None
    exam = profile.exam_date if profile else None
    days = (exam - timezone.localdate()).days if exam else None

    attempts = list(Attempt.objects.filter(user=request.user).order_by("-created_at")[:READING_RECENT])
    weaknesses = detect_weaknesses(subs, target, reading_attempts=attempts)
    plan = build_today(request.user, weaknesses, has_essays=bool(subs), days_to_exam=days)
    return Response({"essays_analysed": len(subs), "weaknesses": weaknesses, "plan": plan})


def _context(request):
    subs = list(
        Submission.objects.filter(user=request.user, status=Submission.Status.DONE)
        .select_related("prompt").order_by("-created_at")[:RECENT]
    )
    profile = getattr(request.user, "profile", None)
    exam = profile.exam_date if profile else None
    days = (exam - timezone.localdate()).days if exam else None
    attempts = list(Attempt.objects.filter(user=request.user).order_by("-created_at")[:READING_RECENT])
    weaknesses = detect_weaknesses(subs, profile.target_band if profile else None, reading_attempts=attempts)
    return subs, weaknesses, days


@extend_schema(responses=OpenApiTypes.OBJECT, summary="This week's study plan, with what was done on past days")
@api_view(["GET"])
def week(request):
    """T3.4: lịch tuần; ngày đã qua hiện việc đã làm, hôm nay = kế hoạch hôm nay, ngày tới xếp theo quy tắc."""
    subs, weaknesses, days = _context(request)
    data = build_week(request.user, weaknesses, has_essays=bool(subs), days_to_exam=days)
    data["weaknesses"] = weaknesses
    return Response(data)
