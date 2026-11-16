"""Chấm Reading tự động + quy đổi band (T1.5, REA-06).

Quy đổi theo bảng Academic Reading phổ biến (thang 40 câu). Một bài đọc lẻ có ít câu hơn
nên số câu đúng được quy về thang 40 trước khi tra bảng -> chỉ là ước lượng, ghi rõ trên giao diện.
"""
import re

# (số câu đúng tối thiểu trên 40, band)
ACADEMIC_BANDS = [
    (39, 9.0), (37, 8.5), (35, 8.0), (33, 7.5), (30, 7.0), (27, 6.5), (23, 6.0),
    (19, 5.5), (15, 5.0), (13, 4.5), (10, 4.0), (8, 3.5), (6, 3.0), (4, 2.5),
]
NOT_GIVEN = {"not given", "ng", "notgiven"}


def normalise(value) -> str:
    text = str(value or "").lower().strip()
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"[^\w\s'-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _canonical(kind: str, value: str) -> str:
    text = normalise(value)
    if kind in ("tfng", "ynng"):
        if text in NOT_GIVEN:
            return "not given"
        return {"t": "true", "f": "false", "y": "yes", "n": "no"}.get(text, text)
    return text


def is_correct(kind: str, answers: list[str], given, max_words: int | None = None) -> bool:
    given_text = _canonical(kind, given)
    if not given_text:
        return False
    if kind == "completion":
        if max_words and len(given_text.split()) > max_words:
            return False  # viết quá số từ cho phép là sai, như thi thật
        given_text = re.sub(r"^(the|a|an) ", "", given_text)
        return any(given_text == re.sub(r"^(the|a|an) ", "", normalise(a)) for a in answers)
    return any(given_text == _canonical(kind, a) for a in answers)


def band_from_score(correct: int, total: int) -> float:
    if total <= 0:
        return 0.0
    scaled = round(correct * 40 / total)
    for minimum, band in ACADEMIC_BANDS:
        if scaled >= minimum:
            return band
    return 0.0 if scaled == 0 else 2.0


def grade(passage, answers: dict) -> dict:
    """answers: {"1": "TRUE", ...} -> {"results": [...], "correct": n, "total": m, "band": b}"""
    results, correct, total = [], 0, 0
    for group in passage.groups.all():
        for q in group.questions.all():
            given = answers.get(str(q.number), "")
            ok = is_correct(group.kind, q.answers, given, group.max_words)
            correct += ok
            total += 1
            results.append({
                "number": q.number,
                "kind": group.kind,
                "given": given,
                "correct": ok,
                "answer": q.answers[0],
                "explanation": q.explanation,
                "evidence": q.evidence,
            })
    return {"results": results, "correct": correct, "total": total, "band": band_from_score(correct, total)}
