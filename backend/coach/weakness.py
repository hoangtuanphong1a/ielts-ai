"""Phát hiện điểm yếu (T3.3, DASH-06) từ các bài Writing đã chấm gần đây.

Gộp 3 nguồn bằng chứng, mỗi điểm yếu có số liệu đi kèm:
1. Nhóm lỗi lặp lại (từ `issues` của LanguageTool + spaCy): hoà hợp S-V, mạo từ, chính tả...
   tính theo số lỗi / 100 từ trên tổng các bài.
2. Đặc trưng NLP trung bình (từ `features`): bài ngắn, ít từ học thuật, ít câu phức,
   ít từ nối, thiếu đoạn, có đoạn lạc đề.
3. Tiêu chí band thấp so với mục tiêu (hoặc so với band chung nếu chưa đặt mục tiêu).

Mỗi ứng viên có `severity` (càng lớn càng cần ưu tiên); trả top N, không trùng tiêu chí
khi có thể, để học viên thấy 3 việc khác nhau.
"""
import re
from dataclasses import asdict, dataclass, field

RECENT = 10          # số bài gần nhất dùng để phân tích
MIN_WORDS = {"task1": 150, "task2": 250}

CRITERIA = {
    "task_response": "Task Response",
    "coherence": "Coherence & Cohesion",
    "lexical": "Lexical Resource",
    "grammar": "Grammatical Range & Accuracy",
    "reading": "Reading",
}
WRITING_CRITERIA = ["task_response", "coherence", "lexical", "grammar"]

# Reading: dạng câu hỏi -> (nhãn, mẹo). Dạng làm đúng < 60% (ít nhất 4 câu) thành điểm yếu.
READING_KINDS = {
    "tfng": ("True / False / Not Given",
             "FALSE means the passage says the opposite. NOT GIVEN means it says nothing about it. "
             "Find the exact sentence before you choose."),
    "ynng": ("Yes / No / Not Given",
             "Look for the writer's opinion words (in my view, should, too slow). If the writer never comments, it is NOT GIVEN."),
    "headings": ("Matching headings",
                 "Read the first and last sentences of each paragraph and match the main idea, not a single shared word."),
    "match_info": ("Matching information",
                   "Scan for a specific detail such as a number, an example or a reason, not the general topic."),
    "mcq": ("Multiple choice",
            "Rule out options that are true in the passage but do not answer the question."),
    "completion": ("Sentence completion",
                   "Copy the words exactly from the passage and keep to the word limit; extra words make the answer wrong."),
}
READING_RECENT = 5
READING_MIN_QUESTIONS = 4
READING_WEAK = 0.6

# Nhóm lỗi: (nhãn, tiêu chí, ngưỡng lỗi/100 từ để coi là điểm yếu, mức "rất nặng", mẹo)
ERROR_GROUPS = {
    "agreement": ("Subject-verb agreement", "grammar", 0.4, 1.5,
                  "Find the subject of each verb. Singular subjects (he, it, this, working) take -s: "
                  "“people work”, “it works”."),
    "articles": ("Articles (a / an / the)", "grammar", 0.4, 1.5,
                 "Use “an” before a vowel sound, “a” before a consonant sound, and “the” "
                 "for something already mentioned or unique."),
    "verb_form": ("Verb forms and tenses", "grammar", 0.4, 1.5,
                  "Check each verb: past events need past forms, and modal verbs (can, should) "
                  "are followed by the base form."),
    "spelling": ("Spelling and word choice", "lexical", 1.0, 3.0,
                 "Proofread for common slips (there / their, dont / don't) and learn the spelling "
                 "of words you use often."),
    "punctuation": ("Punctuation", "grammar", 1.5, 4.0,
                    "Put a comma after linking words at the start of a sentence "
                    "(However, ... / Firstly, ...)."),
}
AGREEMENT_RULES = re.compile(r"AGREEMENT|AGR\b|NON3PRS|SOME_NN_VBP|_VBZ|_VBP")
ARTICLE_RULES = re.compile(r"A_VS_AN|DETERMINER|ARTICLE|_THE_|^THE_")
VERB_RULES = re.compile(r"TENSE|VERB_FORM|MD_BASEFORM|BASE_FORM|PAST|PARTICIPLE|GERUND|_VB\b")


def group_of(issue: dict) -> str | None:
    rule, category = issue.get("rule", ""), issue.get("category")
    if AGREEMENT_RULES.search(rule):
        return "agreement"
    if ARTICLE_RULES.search(rule):
        return "articles"
    if category == "grammar" and VERB_RULES.search(rule):
        return "verb_form"
    if category == "spelling":
        return "spelling"
    if category == "punctuation":
        return "punctuation"
    return None  # lỗi văn phong và lỗi ngữ pháp khác: chưa đủ cụ thể để thành bài tập


@dataclass
class Weakness:
    key: str
    title: str
    criterion: str
    evidence: str
    tip: str
    severity: float
    examples: list = field(default_factory=list)

    def as_dict(self):
        data = asdict(self)
        data["criterion_label"] = CRITERIA[self.criterion]
        data["severity"] = round(self.severity, 2)
        return data


def sentence_around(text: str, offset: int, length: int) -> tuple[str, int]:
    """Câu chứa lỗi và vị trí lỗi trong câu đó."""
    start = max(text.rfind(ch, 0, offset) for ch in ".!?\n") + 1
    ends = [i for i in (text.find(ch, offset + length) for ch in ".!?\n") if i != -1]
    end = min(ends) + 1 if ends else len(text)
    while start < offset and text[start].isspace():
        start += 1
    return text[start:end].strip(), offset - start


def error_examples(subs, group: str, limit: int = 3) -> list[dict]:
    """Câu sai thật trong bài của học viên, dùng làm bài tập "tự sửa lỗi của mình"."""
    examples, seen = [], set()
    for sub in subs:  # mới nhất trước
        for issue in sub.issues or []:
            if group_of(issue) != group or not issue.get("replacements"):
                continue
            sentence, at = sentence_around(sub.essay, issue["offset"], issue["length"])
            if sentence in seen or len(sentence) > 240:
                continue
            seen.add(sentence)
            examples.append({
                "submission": sub.id,
                "sentence": sentence,
                "start": at,
                "length": issue["length"],
                "fix": issue["replacements"][0],
                "message": issue.get("message", ""),
            })
            if len(examples) >= limit:
                return examples
    return examples


def _avg(subs, key):
    values = [s.features.get(key) for s in subs if isinstance(s.features.get(key), (int, float))]
    return sum(values) / len(values) if values else None


def _feature_candidates(subs) -> list[Weakness]:
    out = []
    task_type = subs[0].prompt.task_type
    min_words = MIN_WORDS.get(task_type, 250)

    words = _avg(subs, "word_count")
    if words is not None and words < min_words:
        out.append(Weakness(
            "length", "Essay length", "task_response",
            f"Your recent essays average {words:.0f} words. {task_type.replace('task', 'Task ')} needs at least {min_words}.",
            "Plan 4 paragraphs before you write and give each body paragraph an explanation and an example.",
            severity=3 * (1 - words / min_words) + 0.6,
        ))

    awl = _avg(subs, "awl_ratio")
    if awl is not None and awl < 0.10:
        out.append(Weakness(
            "academic_vocab", "Academic vocabulary", "lexical",
            f"Only {awl * 100:.0f}% of your content words are academic words (aim for 10% or more).",
            "Swap everyday words for academic ones: get → obtain, show → indicate, big → significant.",
            severity=(0.10 - awl) * 10 + 0.3,
        ))

    complex_ratio = _avg(subs, "complex_sentence_ratio")
    if complex_ratio is not None and complex_ratio < 0.35:
        out.append(Weakness(
            "complex_sentences", "Complex sentences", "grammar",
            f"{complex_ratio * 100:.0f}% of your sentences are complex (aim for 40% or more).",
            "Join two short ideas with although, which, because or while.",
            severity=(0.35 - complex_ratio) * 3 + 0.3,
        ))

    linkers = _avg(subs, "linker_variety")
    if linkers is not None and linkers < 4:
        out.append(Weakness(
            "linking", "Linking words", "coherence",
            f"You use about {linkers:.0f} different linking words per essay (aim for 5 or more).",
            "Vary your linkers: However, Moreover, As a result, For instance, In contrast.",
            severity=(4 - linkers) * 0.3 + 0.3,
        ))

    paragraphs = _avg(subs, "paragraph_count")
    if task_type == "task2" and paragraphs is not None and paragraphs < 3.5:
        out.append(Weakness(
            "paragraphing", "Paragraph structure", "coherence",
            f"Your essays have {paragraphs:.1f} paragraphs on average (aim for 4 to 5).",
            "Use an introduction, two or three body paragraphs and a conclusion, separated by blank lines.",
            severity=(4 - paragraphs) * 0.4 + 0.3,
        ))

    drifting = sum(len((s.features.get("semantic") or {}).get("off_topic_paragraphs", [])) for s in subs)
    if drifting:
        out.append(Weakness(
            "off_topic", "Staying on topic", "task_response",
            f"{drifting} paragraph{'s' if drifting > 1 else ''} in your recent essays drifted away from the question.",
            "Before each body paragraph, check its first sentence answers the question directly.",
            severity=0.8 + 0.3 * drifting,
        ))
    return out


def _error_candidates(subs) -> list[Weakness]:
    total_words = sum(s.word_count for s in subs) or 1
    counts = {}
    for sub in subs:
        for issue in sub.issues or []:
            group = group_of(issue)
            if group:
                counts[group] = counts.get(group, 0) + 1

    out = []
    for group, n in counts.items():
        label, criterion, threshold, heavy, tip = ERROR_GROUPS[group]
        rate = n * 100 / total_words
        if rate < threshold:
            continue
        out.append(Weakness(
            group, label, criterion,
            f"{n} {label.lower()} error{'s' if n > 1 else ''} in your last {len(subs)} essay{'s' if len(subs) > 1 else ''} "
            f"({rate:.1f} per 100 words).",
            tip,
            severity=0.5 + rate / heavy,
            examples=error_examples(subs, group),
        ))
    return out


def _criterion_candidates(subs, target: float | None) -> list[Weakness]:
    averages = {k: sum(getattr(s, f"band_{k}") for s in subs) / len(subs) for k in WRITING_CRITERIA}
    overall = sum(s.band_overall for s in subs) / len(subs)
    reference = target if target is not None else overall
    out = []
    for key, avg in averages.items():
        gap = reference - avg
        if gap >= 0.5:
            out.append(Weakness(
                f"criterion_{key}", CRITERIA[key], key,
                f"Your average {CRITERIA[key]} is {avg:.1f}, "
                + (f"{gap:.1f} below your target of {target:.1f}." if target is not None
                   else f"{gap:.1f} below your overall band."),
                "Open your weakest essay and compare it with the feedback for this criterion.",
                severity=gap * 0.6,
            ))
    return out


def _reading_candidates(attempts) -> list[Weakness]:
    stats = {}
    for attempt in attempts:
        for r in attempt.results:
            right, total = stats.get(r["kind"], (0, 0))
            stats[r["kind"]] = (right + bool(r["correct"]), total + 1)
    out = []
    for kind, (right, total) in stats.items():
        accuracy = right / total
        if kind not in READING_KINDS or total < READING_MIN_QUESTIONS or accuracy >= READING_WEAK:
            continue
        label, tip = READING_KINDS[kind]
        out.append(Weakness(
            f"reading_{kind}", f"{label} questions", "reading",
            f"{right} of {total} correct in your last {len(attempts)} reading attempt{'s' if len(attempts) > 1 else ''} "
            f"({accuracy * 100:.0f}%).",
            tip,
            severity=(READING_WEAK - accuracy) * 3 + 0.5,
        ))
    return out


def detect_weaknesses(subs: list, target: float | None = None, top: int = 3,
                      reading_attempts: list | None = None) -> list[dict]:
    """`subs`: các Submission đã chấm, mới nhất trước; `reading_attempts`: lượt Reading gần nhất."""
    subs = list(subs)[:RECENT]
    attempts = list(reading_attempts or [])[:READING_RECENT]
    if not subs and not attempts:
        return []
    candidates = _reading_candidates(attempts)
    if subs:
        writing = _error_candidates(subs) + _feature_candidates(subs)
        specific_criteria = {c.criterion for c in writing}
        # Tiêu chí thấp chỉ thêm khi chưa có điểm yếu cụ thể nào giải thích nó
        writing += [c for c in _criterion_candidates(subs, target) if c.criterion not in specific_criteria]
        candidates += writing
    candidates.sort(key=lambda c: c.severity, reverse=True)

    picked, used = [], set()
    for c in candidates:  # lượt 1: mỗi tiêu chí một điểm yếu
        if c.criterion not in used:
            picked.append(c)
            used.add(c.criterion)
        if len(picked) == top:
            break
    for c in candidates:  # lượt 2: còn chỗ thì lấy tiếp theo mức độ
        if len(picked) == top:
            break
        if c not in picked:
            picked.append(c)
    return [c.as_dict() for c in picked]
