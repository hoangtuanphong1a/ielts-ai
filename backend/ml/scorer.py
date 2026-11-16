"""Chấm band IELTS Writing.

- Có file model (ml/artifacts/band_model.joblib) -> model dự đoán band overall.
- Không có -> heuristic dựa trên đặc trưng NLP.
4 tiêu chí (TR, CC, LR, GRA) luôn là ước lượng heuristic.
"""
import math
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .features import extract_features
from .grammar import error_rates
from .lexical import lexical_profile
from .semantic import semantic_profile

MIN_WORDS = {"task1": 150, "task2": 250}
OFF_TOPIC_RELEVANCE = 0.15  # cả bài gần như không liên quan đến đề


def round_band(x: float) -> float:
    """Làm tròn theo quy tắc IELTS: .25 -> .5, .75 -> lên 1."""
    x = max(0.0, min(9.0, x))
    return math.floor(x * 2 + 0.5) / 2


def _scale(value: float, low: float, high: float) -> float:
    """Đưa value về [0, 1] theo khoảng [low, high]."""
    if high == low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


@dataclass
class ScoreResult:
    overall: float
    task_response: float
    coherence: float
    lexical: float
    grammar: float
    feedback: list[str] = field(default_factory=list)
    features: dict = field(default_factory=dict)
    scorer: str = "heuristic"


def length_cap(word_count: float, task_type: str) -> float:
    """Band tối đa theo độ dài bài. Thiếu từ là lỗi Task Response nặng trong IELTS,
    nên câu chữ tốt cũng không bù được."""
    ratio = word_count / MIN_WORDS.get(task_type, 250)
    if ratio >= 1:
        return 9.0
    if ratio >= 0.8:
        return 6.5
    if ratio >= 0.6:
        return 5.5
    return 4.5


def heuristic_criteria(f: dict, task_type: str) -> dict[str, float]:
    min_words = MIN_WORDS.get(task_type, 250)

    if "semantic_relevance" in f:
        # T2.4: độ bám đề theo nghĩa (Sentence-BERT) thay cho đếm từ trùng với đề.
        # Chỉ phân biệt đúng đề / lạc đề, nên bão hoà sớm (>= 0.45 là đủ điểm).
        tr = 4 + 3 * _scale(f["word_count"], min_words * 0.6, min_words) \
               + 2 * _scale(f["semantic_relevance"], 0.15, 0.45)
        cc = 4 + 2 * _scale(f["paragraph_count"], 1, 4) \
               + 1.5 * _scale(f["linker_variety"], 1, 7) \
               + 0.5 * _scale(f["avg_sentence_len"], 10, 20) \
               + 1 * _scale(f["topic_continuity"], 0.15, 0.35) \
               - 1.5 * _scale(f["paragraph_redundancy"], 0.85, 0.97)
    else:
        tr = 4 + 3 * _scale(f["word_count"], min_words * 0.6, min_words) \
               + 2 * _scale(f["prompt_overlap"], 0.1, 0.6)
        cc = 4 + 2 * _scale(f["paragraph_count"], 1, 4) \
               + 2 * _scale(f["linker_variety"], 1, 7) \
               + 1 * _scale(f["avg_sentence_len"], 10, 20)
    if "awl_ratio" in f:
        # T2.2: có spaCy -> dùng từ học thuật (AWL) và từ ít phổ biến thay cho "từ dài"
        lr = 4 + 2 * _scale(f["guiraud_index"], 5, 10) \
               + 1.5 * _scale(f["awl_ratio"], 0.04, 0.25) \
               + 1.5 * _scale(f["advanced_ratio"], 0.03, 0.20) \
               - 1 * _scale(f["top_word_repeat_ratio"], 0.04, 0.10)
    else:
        lr = 4 + 3 * _scale(f["guiraud_index"], 5, 10) \
               + 2 * _scale(f["long_word_ratio"], 0.12, 0.30) \
               - 1 * _scale(f["top_word_repeat_ratio"], 0.04, 0.10)
    gra = 4 + 3 * _scale(f["complex_sentence_ratio"], 0.2, 0.7) \
            + 2 * _scale(f["avg_sentence_len"], 10, 22)

    return {
        "task_response": round_band(tr),
        "coherence": round_band(cc),
        "lexical": round_band(lr),
        "grammar": round_band(gra),
    }


def build_feedback(f: dict, task_type: str) -> list[str]:
    tips = []
    min_words = MIN_WORDS.get(task_type, 250)
    if f["word_count"] < min_words:
        tips.append(f"Your essay has {int(f['word_count'])} words. Write at least {min_words}.")
    if f["paragraph_count"] < 4 and task_type == "task2":
        tips.append("Use 4 to 5 paragraphs: introduction, 2 to 3 body paragraphs, conclusion.")
    if f["linker_variety"] < 4:
        tips.append("Use a wider range of linking words (However, Moreover, Consequently...).")
    if f["top_word_repeat_ratio"] > 0.08:
        tips.append("One word is repeated too often. Try synonyms.")
    if f["complex_sentence_ratio"] < 0.3:
        tips.append("Add complex sentences (although, which, because...) to lift your grammar score.")
    if "awl_ratio" in f and f["awl_ratio"] < 0.08:
        tips.append("Use more academic vocabulary, for example: significant, contribute, approach, impact.")
    if "advanced_ratio" in f and f["advanced_ratio"] < 0.05:
        tips.append("Most of your words are very common. Replace a few with more precise, less common words.")
    if "semantic_relevance" in f:
        if f["semantic_relevance"] < OFF_TOPIC_RELEVANCE:
            # Lỗi nặng nhất -> đưa lên đầu danh sách
            tips.insert(0, "Your essay does not seem to answer this question. Read the prompt again and respond to it directly.")
        if f.get("paragraph_redundancy", 0) > 0.9:
            tips.append("Two of your paragraphs say almost the same thing. Give each paragraph its own main idea.")
    elif f["prompt_overlap"] < 0.2:
        tips.append("Your essay may be off topic. Stay close to the key words in the question.")
    if not tips:
        tips.append("Well balanced. Next, check grammar accuracy and word choice.")
    return tips


@lru_cache(maxsize=1)
def _load_model(path: str):
    p = Path(path)
    if not p.exists():
        return None
    import joblib

    return joblib.load(p)


def score_essay(essay: str, prompt: str = "", task_type: str = "task2",
                model_path: str | None = None, grammar_issues: list | None = None) -> ScoreResult:
    f = extract_features(essay, prompt)
    lex = lexical_profile(essay)
    if lex:
        f.update(lex["features"])
    sem = semantic_profile(essay, prompt)
    if sem:
        f.update(sem["features"])
    criteria = heuristic_criteria(f, task_type)
    extra_tips = []

    # T2.3: lỗi thật từ LanguageTool -> trừ Grammatical Range (ngữ pháp) và Lexical Resource (chính tả)
    if grammar_issues:
        rates = error_rates(grammar_issues, f["word_count"])
        f.update(rates)
        criteria["grammar"] = round_band(criteria["grammar"] - min(3.0, rates["grammar_per_100"] * 0.6))
        criteria["lexical"] = round_band(criteria["lexical"] - min(1.5, rates["spelling_per_100"] * 0.4))
        if rates["grammar_per_100"] >= 2:
            extra_tips.append(f"About {rates['grammar_per_100']:.0f} grammar mistakes per 100 words. Review the highlighted sentences.")
        if rates["spelling_per_100"] >= 1:
            extra_tips.append("Several spelling mistakes lower your Lexical Resource. Check the highlighted words.")

    model = _load_model(str(model_path)) if model_path else None
    if model is not None:
        overall = round_band(float(model.predict([essay])[0]))
        scorer = "model"
    else:
        overall = round_band(sum(criteria.values()) / 4)
        scorer = "heuristic"

    # Áp trần độ dài cho cả model lẫn heuristic
    cap = length_cap(f["word_count"], task_type)
    overall = min(overall, cap)
    criteria["task_response"] = min(criteria["task_response"], cap)

    # Lạc đề hoàn toàn: IELTS chấm Task Response rất thấp dù câu chữ tốt
    if sem and f["semantic_relevance"] < OFF_TOPIC_RELEVANCE:
        criteria["task_response"] = min(criteria["task_response"], 4.0)
        overall = min(overall, 4.5)

    extra = {}
    if lex:
        extra["vocab"] = lex["profile"]
    if sem:
        extra["semantic"] = sem["detail"]
        drifting = sem["detail"]["off_topic_paragraphs"]
        # Chỉ nêu đoạn lạc đề khi phần còn lại đúng đề (cả bài lạc đề đã có gợi ý riêng)
        if drifting and f["semantic_relevance"] >= OFF_TOPIC_RELEVANCE:
            extra_tips.append(f"Paragraph {', '.join(map(str, drifting))} drifts away from the question. Link it back to the topic.")

    return ScoreResult(
        overall=overall,
        feedback=extra_tips + build_feedback(f, task_type),
        features={**f, **extra},
        scorer=scorer,
        **criteria,
    )
