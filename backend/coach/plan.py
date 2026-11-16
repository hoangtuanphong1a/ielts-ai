"""Kế hoạch học hôm nay (một phần T3.4) và đề xuất đề (T3.5, content-based).

Ngân sách = số phút học mỗi ngày học viên tự đặt (Profile.daily_minutes).
Thứ tự ưu tiên:
1. Chưa có bài nào -> viết bài chẩn đoán trước tiên (không có dữ liệu thì không cá nhân hoá được).
2. Tự sửa lỗi của chính mình (câu sai thật trong bài) cho điểm yếu số 1.
3. Ôn thẻ từ vựng đến hạn (SM-2).
4. Viết: đủ 40 phút -> cả bài; đủ 15 phút -> một đoạn thân bài theo điểm yếu.
Gần ngày thi (<= 14 ngày) -> viết bài có bấm giờ được đẩy lên trước ôn từ.
"""
from django.db.models import Max
from django.utils import timezone

from vocab.models import Card, Word
from vocab.views import DAILY_TARGET
from reading.models import Passage
from writing.models import WritingPrompt

ESSAY_MINUTES = {"task1": 20, "task2": 40}
PARAGRAPH_MINUTES = 15
DRILL_MINUTES = 5
VOCAB_MINUTES = 10
EXAM_SOON_DAYS = 14


def recommend_passage(user) -> dict | None:
    """Bài đọc chưa làm trước; làm hết rồi thì bài có band tốt nhất thấp nhất."""
    untried = Passage.objects.exclude(attempts__user=user).order_by("id").first()
    if untried:
        return {"id": untried.id, "title": untried.title, "minutes": untried.minutes,
                "reason": "A passage you have not tried yet."}
    weakest = (Passage.objects.filter(attempts__user=user)
               .annotate(best=Max("attempts__band")).order_by("best").first())
    if weakest:
        return {"id": weakest.id, "title": weakest.title, "minutes": weakest.minutes,
                "reason": f"Your best band here is {weakest.best:.1f}. Try it again."}
    return None


def recommend_prompt(user, task_type: str | None = None) -> dict | None:
    """Đề chưa làm (ưu tiên đúng dạng bài); làm hết rồi thì làm lại đề có band tốt nhất thấp nhất."""
    prompts = WritingPrompt.objects.all()
    if task_type:
        same_type = prompts.filter(task_type=task_type)
        prompts = same_type if same_type.exists() else prompts
    untried = prompts.exclude(submissions__user=user).order_by("id").first()
    if untried:
        return {"id": untried.id, "title": untried.title, "task_type": untried.task_type,
                "reason": "A new question you have not tried yet."}
    weakest = (prompts.filter(submissions__user=user, submissions__status="done")
               .annotate(best=Max("submissions__band_overall")).order_by("best").first())
    if weakest:
        return {"id": weakest.id, "title": weakest.title, "task_type": weakest.task_type,
                "reason": f"Your best band here is {weakest.best:.1f}. Rewrite it with today's focus in mind."}
    return None


def vocab_due(user) -> int:
    today = timezone.localdate()
    due = Card.objects.filter(user=user, due_date__lte=today).count()
    if due >= DAILY_TARGET:
        return DAILY_TARGET
    new_words = Word.objects.filter(added_by__isnull=True).exclude(cards__user=user).count()
    return due + min(new_words, DAILY_TARGET - due)


def build_today(user, weaknesses: list[dict], has_essays: bool, days_to_exam: int | None) -> dict:
    budget = getattr(getattr(user, "profile", None), "daily_minutes", None) or 30
    focus = weaknesses[0] if weaknesses else None
    prompt = recommend_prompt(user)
    candidates = []

    if not has_essays:
        candidates.append({
            "kind": "diagnostic", "minutes": ESSAY_MINUTES.get(prompt["task_type"] if prompt else "task2", 40),
            "title": "Write your first essay",
            "detail": "One essay lets us find your strengths and weaknesses and personalise this plan.",
            "prompt": prompt,
        })

    if focus and focus.get("examples"):
        candidates.append({
            "kind": "drill", "minutes": DRILL_MINUTES,
            "title": f"Fix your own mistakes: {focus['title'].lower()}",
            "detail": f"{len(focus['examples'])} sentences from your essays. Find the error, then check the fix.",
            "examples": focus["examples"],
        })

    due = vocab_due(user)
    vocab_item = {
        "kind": "vocab", "minutes": VOCAB_MINUTES, "count": due,
        "title": f"Review {due} vocabulary card{'s' if due != 1 else ''}",
        "detail": "Spaced repetition brings each word back just before you forget it.",
    } if due else None
    exam_soon = days_to_exam is not None and 0 <= days_to_exam <= EXAM_SOON_DAYS

    def writing_item(minutes_left: int):
        """Viết cả bài nếu đủ thời gian, không thì một đoạn thân bài, không đủ nữa thì bỏ."""
        if not (has_essays and prompt):
            return None
        essay_minutes = ESSAY_MINUTES.get(prompt["task_type"], 40)
        if minutes_left >= essay_minutes:
            return {
                "kind": "essay", "minutes": essay_minutes,
                "title": "Timed essay" if exam_soon else "Write a full essay",
                "detail": (f"Keep today's focus in mind: {focus['title'].lower()}." if focus else prompt["reason"]),
                "prompt": prompt,
            }
        if minutes_left >= PARAGRAPH_MINUTES:
            return {
                "kind": "paragraph", "minutes": PARAGRAPH_MINUTES,
                "title": "Write one body paragraph",
                "detail": (f"Practise {focus['title'].lower()} in a single paragraph." if focus
                           else "Practise one clear idea with an explanation and an example."),
                "prompt": prompt,
            }
        return None

    plan = [item for item in candidates if item]
    used = sum(item["minutes"] for item in plan)
    essay_minutes = ESSAY_MINUTES.get(prompt["task_type"], 40) if prompt else 40
    if exam_soon or budget - used >= essay_minutes:
        # Đủ thời gian (hoặc sắp thi): viết trước, ôn từ nếu còn chỗ
        order = [writing_item, lambda left: vocab_item]
    else:
        # Ít thời gian: ôn từ trước nếu vẫn còn chỗ cho một đoạn văn
        order = [lambda left: vocab_item if left - VOCAB_MINUTES >= PARAGRAPH_MINUTES or not has_essays else None,
                 writing_item, lambda left: vocab_item]
    # Reading: khi còn thời gian, hoặc khi điểm yếu số 1 là một dạng câu hỏi Reading
    passage = recommend_passage(user)
    reading_focus = bool(focus) and focus.get("criterion") == "reading"
    reading_item = {
        "kind": "reading", "minutes": passage["minutes"], "passage": passage,
        "title": "Reading practice",
        "detail": (f"Watch out for {focus['title'].lower()}. {passage['reason']}" if reading_focus else passage["reason"]),
    } if passage else None
    if reading_focus:
        order.insert(0, lambda left: reading_item)
    else:
        order.append(lambda left: reading_item)

    for make in order:
        item = make(budget - used)
        if item and item not in plan and (used + item["minutes"] <= budget or not plan):
            plan.append(item)
            used += item["minutes"]
    return {"budget": budget, "minutes": used, "items": plan, "focus": focus, "recommended_prompt": prompt}
