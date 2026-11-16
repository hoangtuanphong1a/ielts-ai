"""Kiểm tra hoà hợp chủ ngữ - động từ bằng spaCy (T2.3, bổ sung cho LanguageTool).

LanguageTool bản docker không có dữ liệu ngram nên bỏ sót lỗi kiểu "people works",
"this have", "working from home are". spaCy cho cây phụ thuộc (ai là chủ ngữ của động
từ nào) và số ít / số nhiều, nên bắt được các lỗi này.

Chỉ xét động từ chia ở hiện tại (VBZ / VBP) và was / were. Trường hợp mơ hồ thì bỏ qua:
thà sót lỗi còn hơn báo sai cho học viên.
spaCy chưa cài -> trả [] để việc chấm vẫn chạy.
"""
from .nlp import get_nlp

# Đại từ đi với động từ dạng "số nhiều" (I work, you work, they work)
PLURAL_PRONOUNS = {"i", "you", "we", "they", "these", "those"}
SINGULAR_PRONOUNS = {
    "he", "she", "it", "this", "that", "everyone", "everybody", "someone", "somebody",
    "anyone", "anybody", "nobody", "everything", "something", "nothing", "each",
}
# Chủ ngữ không rõ số (some / all / most ... + of, đại từ quan hệ): bỏ qua
AMBIGUOUS = {"some", "all", "most", "none", "any", "more", "half", "who", "which", "what"}
IRREGULAR_TO_PLURAL = {"is": "are", "was": "were", "has": "have", "does": "do"}
IRREGULAR_TO_SINGULAR = {"are": "is", "were": "was", "have": "has", "do": "does", "am": "is"}


def _subject_number(subj) -> str | None:
    """'sing' | 'plur' | None (không chắc)."""
    word = subj.lower_
    if any(child.dep_ == "conj" for child in subj.children):
        return "plur"  # "Students and teachers ..."
    if word in PLURAL_PRONOUNS:
        return "plur"
    if word in AMBIGUOUS or subj.tag_ in {"WDT", "WP"}:
        return None  # "that" làm đại từ quan hệ có tag WDT -> bỏ qua ở đây
    if word in SINGULAR_PRONOUNS:
        return "sing"
    if any(child.dep_ == "prep" and child.lower_ == "of" for child in subj.children):
        return None  # "the number of students", "one of the reasons": dễ sai, bỏ qua
    if subj.tag_ in {"NNS", "NNPS"}:
        return "plur"
    if subj.tag_ in {"NN", "NNP", "VBG"}:
        return "sing"  # danh từ số ít, hoặc danh động từ "Working from home ..."
    return None


def _finite_verb(subj):
    """Động từ chia thì hiện tại / was-were mà chủ ngữ này quyết định."""
    head = subj.head
    candidates = [head] + [c for c in head.children if c.dep_ in {"aux", "auxpass"}]
    for tok in candidates:
        if tok.tag_ in {"VBZ", "VBP"} or tok.lower_ in {"was", "were"}:
            return tok
    # spaCy hay gắn nhãn VB cho "My brother go ...". Động từ gốc câu có chủ ngữ mà không có
    # trợ động từ thì thực chất là động từ chia hiện tại. Bỏ qua mệnh đề phụ (ccomp) để tránh
    # thức giả định kiểu "I suggest he go".
    if (head.tag_ == "VB" and head.dep_ in {"ROOT", "conj"} and len(candidates) == 1
            and not any(c.dep_ == "mark" for c in head.children)):
        return head
    return None


def _to_plural(verb) -> str:
    return IRREGULAR_TO_PLURAL.get(verb.lower_) or str(verb.lemma_)


def _to_singular(verb) -> str:
    word = verb.lower_
    if word in IRREGULAR_TO_SINGULAR:
        return IRREGULAR_TO_SINGULAR[word]
    base = verb.lemma_
    if base.endswith(("s", "sh", "ch", "x", "z", "o")):
        return base + "es"
    if base.endswith("y") and len(base) > 1 and base[-2] not in "aeiou":
        return base[:-1] + "ies"
    return base + "s"


def _keep_case(original: str, word: str) -> str:
    return word.capitalize() if original[:1].isupper() else word


def check_agreement(text: str) -> list[dict]:
    nlp = get_nlp()
    if nlp is None or not text.strip():
        return []
    issues = []
    seen = set()
    for subj in nlp(text):
        if subj.dep_ not in {"nsubj", "nsubjpass", "csubj"}:
            continue
        number = _subject_number(subj)
        verb = _finite_verb(subj)
        if number is None or verb is None or verb.i in seen:
            continue
        is_singular_form = verb.tag_ == "VBZ" or verb.lower_ == "was"
        if number == "plur" and is_singular_form:
            fix = _to_plural(verb)
        elif number == "sing" and not is_singular_form:
            fix = _to_singular(verb)
        else:
            continue
        seen.add(verb.i)
        issues.append({
            "offset": verb.idx,
            "length": len(verb.text),
            "category": "grammar",
            "message": f"The verb does not agree with its subject “{subj.text}”.",
            "replacements": [_keep_case(verb.text, fix)],
            "rule": "SPACY_SUBJECT_VERB_AGREEMENT",
        })
    return issues


def merge_issues(primary: list[dict], extra: list[dict]) -> list[dict]:
    """Gộp lỗi, bỏ lỗi của `extra` nếu chồng lên vị trí đã có trong `primary`."""
    taken = [(i["offset"], i["offset"] + i["length"]) for i in primary]
    merged = list(primary)
    for issue in extra:
        start, end = issue["offset"], issue["offset"] + issue["length"]
        if any(start < b and a < end for a, b in taken):
            continue
        merged.append(issue)
        taken.append((start, end))
    return sorted(merged, key=lambda i: i["offset"])
