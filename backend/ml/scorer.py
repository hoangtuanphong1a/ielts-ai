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

MIN_WORDS = {"task1": 150, "task2": 250}


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

    tr = 4 + 3 * _scale(f["word_count"], min_words * 0.6, min_words) \
           + 2 * _scale(f["prompt_overlap"], 0.1, 0.6)
    cc = 4 + 2 * _scale(f["paragraph_count"], 1, 4) \
           + 2 * _scale(f["linker_variety"], 1, 7) \
           + 1 * _scale(f["avg_sentence_len"], 10, 20)
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
        tips.append(f"Bài mới {int(f['word_count'])} từ, cần tối thiểu {min_words} từ.")
    if f["paragraph_count"] < 4 and task_type == "task2":
        tips.append("Nên chia 4-5 đoạn: mở bài, 2-3 thân bài, kết luận.")
    if f["linker_variety"] < 4:
        tips.append("Dùng thêm từ nối đa dạng (However, Moreover, Consequently...).")
    if f["top_word_repeat_ratio"] > 0.08:
        tips.append("Một từ bị lặp quá nhiều, hãy dùng từ đồng nghĩa.")
    if f["complex_sentence_ratio"] < 0.3:
        tips.append("Thêm câu phức (although, which, because...) để tăng điểm ngữ pháp.")
    if f["prompt_overlap"] < 0.2:
        tips.append("Bài có vẻ lệch đề, hãy bám sát từ khoá trong câu hỏi.")
    if not tips:
        tips.append("Bài cân đối. Tiếp theo: kiểm tra lỗi ngữ pháp và độ chính xác từ vựng.")
    return tips


@lru_cache(maxsize=1)
def _load_model(path: str):
    p = Path(path)
    if not p.exists():
        return None
    import joblib

    return joblib.load(p)


def score_essay(essay: str, prompt: str = "", task_type: str = "task2",
                model_path: str | None = None) -> ScoreResult:
    f = extract_features(essay, prompt)
    criteria = heuristic_criteria(f, task_type)

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

    return ScoreResult(
        overall=overall,
        feedback=build_feedback(f, task_type),
        features=f,
        scorer=scorer,
        **criteria,
    )
