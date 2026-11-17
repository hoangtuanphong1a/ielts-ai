"""Lịch học theo tuần (T3.4, AIL-03/AIL-04).

Tuần = thứ Hai -> Chủ nhật hiện tại.
- Ngày đã qua: hiện việc học viên THẬT SỰ đã làm (bài viết, bài đọc, thẻ đã ôn) -> lịch tự cập nhật.
- Hôm nay: đúng kế hoạch của build_today (khớp Dashboard).
- Ngày tới: xếp theo quy tắc trong ngân sách phút/ngày:
  Writing T2/T4/T6 (gần thi: cách ngày, bấm giờ), Reading T3/T5 (+T7 nếu điểm yếu là Reading),
  Chủ nhật ôn tập (viết lại đề band thấp nhất), mỗi ngày tập trung một điểm yếu (xoay vòng top 3),
  thẻ từ vựng ước lượng theo ngày đến hạn thật. Đề / bài đọc đề xuất không lặp giữa các ngày.
"""
from datetime import timedelta

from django.db.models import Max
from django.utils import timezone

from reading.models import Attempt, Passage
from vocab.models import Card, Word
from vocab.views import DAILY_TARGET
from writing.models import Submission, WritingPrompt

from .plan import (DRILL_MINUTES, ESSAY_MINUTES, EXAM_SOON_DAYS, PARAGRAPH_MINUTES, VOCAB_MINUTES,
                   build_today)

WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WRITING_DAYS = {0, 2, 4}
READING_DAYS = {1, 3}
REVIEW_DAY = 6
REWRITE_MINUTES = 20


def _done_on(user, day) -> dict:
    return {
        "essays": Submission.objects.filter(user=user, created_at__date=day, status="done").count(),
        "readings": Attempt.objects.filter(user=user, created_at__date=day).count(),
        "cards": Card.objects.filter(user=user, last_reviewed__date=day).count(),
    }


def _queue_prompts(user) -> list[dict]:
    """Đề chưa làm trước, rồi đề band tốt nhất thấp nhất."""
    untried = [{"id": p.id, "title": p.title, "task_type": p.task_type}
               for p in WritingPrompt.objects.exclude(submissions__user=user).order_by("id")]
    tried = [{"id": p.id, "title": p.title, "task_type": p.task_type}
             for p in WritingPrompt.objects.filter(submissions__user=user, submissions__status="done")
             .annotate(best=Max("submissions__band_overall")).order_by("best").distinct()]
    return untried + tried


def _queue_passages(user) -> list[dict]:
    untried = [{"id": p.id, "title": p.title, "minutes": p.minutes}
               for p in Passage.objects.exclude(attempts__user=user).order_by("id")]
    tried = [{"id": p.id, "title": p.title, "minutes": p.minutes}
             for p in Passage.objects.filter(attempts__user=user).annotate(best=Max("attempts__band")).order_by("best")]
    return untried + tried


def _vocab_on(user, day, today) -> int:
    due = Card.objects.filter(user=user, due_date=day).count() if day > today else 0
    fresh = Word.objects.filter(added_by__isnull=True).exclude(cards__user=user).count()
    return min(DAILY_TARGET, due + fresh)


def _plan_future_day(day, offset, ctx) -> list[dict]:
    budget, weaknesses, exam_days = ctx["budget"], ctx["weaknesses"], ctx["days_to_exam"]
    weekday = day.weekday()
    days_left = None if exam_days is None else exam_days - offset
    exam_soon = days_left is not None and 0 <= days_left <= EXAM_SOON_DAYS
    focus = weaknesses[day.toordinal() % len(weaknesses)] if weaknesses else None
    reading_weak = any(w.get("criterion") == "reading" for w in weaknesses)
    items, used = [], 0

    def add(item):
        nonlocal used
        if used + item["minutes"] <= budget or not items:
            items.append(item)
            used += item["minutes"]

    if focus:
        add({"kind": "drill", "minutes": DRILL_MINUTES, "title": f"Focus: {focus['title'].lower()}",
             "detail": focus["tip"]})

    writing_day = (offset % 2 == 0) if exam_soon else weekday in WRITING_DAYS
    reading_day = weekday in READING_DAYS or (reading_weak and weekday == 5)
    if weekday == REVIEW_DAY and ctx["rewrite"]:
        add({"kind": "paragraph", "minutes": REWRITE_MINUTES, "title": "Review day: rewrite a weak paragraph",
             "detail": "Rewrite one paragraph from your lowest-band essay using this week's focus.",
             "prompt": ctx["rewrite"]})
    elif writing_day and ctx["prompts"]:
        prompt = ctx["prompts"].pop(0)
        essay = ESSAY_MINUTES.get(prompt["task_type"], 40)
        if budget - used >= essay:
            add({"kind": "essay", "minutes": essay, "title": "Timed essay" if exam_soon else "Write a full essay",
                 "detail": prompt["title"], "prompt": prompt})
        else:
            add({"kind": "paragraph", "minutes": PARAGRAPH_MINUTES, "title": "Write one body paragraph",
                 "detail": prompt["title"], "prompt": prompt})
    elif reading_day and ctx["passages"]:
        passage = ctx["passages"].pop(0)
        add({"kind": "reading", "minutes": passage["minutes"], "title": "Reading practice",
             "detail": passage["title"], "passage": passage})

    cards = _vocab_on(ctx["user"], day, ctx["today"])
    if cards:
        add({"kind": "vocab", "minutes": VOCAB_MINUTES, "count": cards,
             "title": f"Review about {cards} vocabulary card{'s' if cards != 1 else ''}",
             "detail": "Cards due that day plus new words."})
    return items


def build_week(user, weaknesses: list[dict], has_essays: bool, days_to_exam: int | None) -> dict:
    today = timezone.localdate()
    monday = today - timedelta(days=today.weekday())
    budget = getattr(getattr(user, "profile", None), "daily_minutes", None) or 30

    today_plan = build_today(user, weaknesses, has_essays, days_to_exam)
    used_prompt = (today_plan["recommended_prompt"] or {}).get("id")
    used_passages = {i["passage"]["id"] for i in today_plan["items"] if i.get("passage")}
    prompts = [p for p in _queue_prompts(user) if p["id"] != used_prompt]
    tried = [p for p in prompts if Submission.objects.filter(user=user, prompt_id=p["id"]).exists()]
    ctx = {
        "user": user, "today": today, "budget": budget, "weaknesses": weaknesses, "days_to_exam": days_to_exam,
        "prompts": prompts,
        "passages": [p for p in _queue_passages(user) if p["id"] not in used_passages],
        "rewrite": tried[0] if tried else None,
    }

    days = []
    for offset_from_monday in range(7):
        day = monday + timedelta(days=offset_from_monday)
        entry = {"date": day.isoformat(), "weekday": WEEKDAY[day.weekday()],
                 "is_today": day == today, "is_past": day < today}
        if day < today:
            entry["done"] = _done_on(user, day)
            entry["items"] = []
        elif day == today:
            entry["done"] = _done_on(user, day)
            entry["items"] = today_plan["items"]
        else:
            entry["items"] = _plan_future_day(day, (day - today).days, ctx) if has_essays else []
        entry["minutes"] = sum(i["minutes"] for i in entry["items"])
        days.append(entry)
    return {"week_start": monday.isoformat(), "budget": budget, "days": days}
