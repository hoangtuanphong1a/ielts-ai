"""Hồ sơ từ vựng của bài viết (T2.2, WRI-11): dùng spaCy + AWL + tần suất từ.

- spaCy: tách từ, gán từ loại (POS), đưa về dạng gốc (lemma).
- AWL (Academic Word List, Coxhead 2000): 570 họ từ học thuật, dữ liệu ở data/awl_headwords.json.
  Danh sách gốc chỉ có từ gốc (headword); dạng phái sinh (analysis, economic, significance...)
  được nhận gần đúng bằng cách so tiền tố. Đây là xấp xỉ, không phải bảng họ từ đầy đủ.
- wordfreq: độ phổ biến Zipf của từ trong tiếng Anh (6 ~ cực phổ biến, 3 ~ hiếm).
  Dùng để ước lượng mức từ: basic / intermediate / advanced.
  Đây là ước lượng theo tần suất, KHÔNG phải nhãn CEFR chính thức.

Chỉ xét từ nội dung (danh, động, tính, trạng từ), bỏ tên riêng, từ dừng, từ sai chính tả.
spaCy hoặc wordfreq chưa cài -> trả None, việc chấm quay về đặc trưng regex cũ.
"""
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .nlp import get_nlp

CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV"}
DATA = Path(__file__).parent / "data" / "awl_headwords.json"

# Ngưỡng Zipf: >= 5.0 từ cơ bản; 4.0 - 5.0 trung cấp; < 4.0 nâng cao
BASIC_ZIPF = 5.0
ADVANCED_ZIPF = 4.0
MIN_PREFIX = 5          # từ gốc ngắn hơn chỉ khớp chính xác (area, data, job...)
MAX_SUFFIX = 6          # đuôi phái sinh dài hơn thì coi là từ khác (survey -> surveillance)
NOT_IN_FAMILY = {"creature", "creatures", "seeker"}


@lru_cache(maxsize=1)
def awl() -> dict[str, int]:
    """{headword: sublist 1..10}"""
    return json.loads(DATA.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _awl_stems() -> list[tuple[str, str]]:
    """(stem, headword), stem dài trước để khớp họ từ cụ thể nhất."""
    stems = []
    for hw in awl():
        if len(hw) >= MIN_PREFIX + 1:
            stem = hw[:-1] if hw.endswith(("e", "y")) else hw
            if hw.endswith(("ant", "ent")):
                stem = hw[:-1]  # significant -> significance, evident -> evidence
            stems.append((stem, hw))
    return sorted(stems, key=lambda s: -len(s[0]))


def _normalise(word: str) -> str:
    """Đưa chính tả Mỹ về Anh như bản AWL: analyze -> analyse, labor -> labour."""
    word = re.sub(r"yz(e|es|ed|ing)$", r"ys\1", word)
    word = re.sub(r"iz(e|es|ed|ing|ation|ations)$", r"is\1", word)
    if word.startswith("labor") and not word.startswith("laborat"):
        word = "labour" + word[5:]
    return word


@lru_cache(maxsize=4096)
def awl_headword(lemma: str) -> str | None:
    word = _normalise(lemma.lower())
    if word in NOT_IN_FAMILY:
        return None
    if word in awl():
        return word
    for stem, hw in _awl_stems():
        if word.startswith(stem) and len(word) - len(stem) <= MAX_SUFFIX:
            return hw
    return None


def _zipf(word: str) -> float:
    from wordfreq import zipf_frequency

    return zipf_frequency(word, "en")


def word_level(lemma: str) -> str | None:
    z = _zipf(lemma)
    if z == 0:
        return None  # không có trong từ điển tần suất: sai chính tả hoặc từ lạ
    if z >= BASIC_ZIPF:
        return "basic"
    if z >= ADVANCED_ZIPF:
        return "intermediate"
    return "advanced"


def lexical_profile(text: str) -> dict | None:
    """Trả {'features': {...số...}, 'profile': {...danh sách từ cho giao diện...}} hoặc None."""
    nlp = get_nlp()
    if nlp is None:
        return None
    try:
        import wordfreq  # noqa: F401
    except ImportError:
        return None

    content = []
    for tok in nlp(text):
        if tok.pos_ in CONTENT_POS and tok.is_alpha and not tok.is_stop and len(tok.text) > 1:
            content.append(tok.lemma_.lower())
    if not content:
        return None

    levels = {}
    academic = Counter()
    for lemma in content:
        level = word_level(lemma)
        if level is None:
            continue
        levels[lemma] = level
        hw = awl_headword(lemma)
        if hw:
            academic[hw] += 1

    known = [lemma for lemma in content if lemma in levels]
    total = max(len(known), 1)
    count = Counter(levels[lemma] for lemma in known)
    advanced_words = sorted({lemma for lemma in known if levels[lemma] == "advanced"}, key=_zipf)

    return {
        "features": {
            "content_word_count": float(len(known)),
            "awl_ratio": sum(academic.values()) / total,
            "awl_families": float(len(academic)),
            "intermediate_ratio": count["intermediate"] / total,
            "advanced_ratio": count["advanced"] / total,
            "lemma_diversity": len(set(known)) / total,
        },
        "profile": {
            "academic_words": [hw for hw, _ in academic.most_common(15)],
            "advanced_words": advanced_words[:15],
            "levels": {k: count[k] for k in ("basic", "intermediate", "advanced")},
        },
    }
