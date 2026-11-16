"""Tra từ offline cho Reading (REA-04): WordNet + spaCy + Sentence-BERT.

- spaCy: đưa từ về dạng gốc (analysing -> analyse) và đoán từ loại theo câu chứa từ.
- WordNet (nltk, dữ liệu ở ml/artifacts/nltk_data): các nghĩa, ví dụ, từ đồng nghĩa.
- Sentence-BERT (ml/semantic.py): xếp nghĩa theo độ gần với câu chứa từ, để "colony" trong bài
  về ong ra nghĩa "a group of organisms living together" thay vì "thuộc địa" (nghĩa phổ biến nhất).
- Kèm mức từ (wordfreq) và họ từ AWL từ ml/lexical.py.

Thiếu nltk / WordNet -> trả None, giao diện báo "No definition found".
"""
import logging
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from .lexical import awl_headword, word_level
from .nlp import get_nlp
from .semantic import embed

logger = logging.getLogger(__name__)

NLTK_DIR = Path(__file__).parent / "artifacts" / "nltk_data"
POS_TO_WN = {"NOUN": "n", "PROPN": "n", "VERB": "v", "AUX": "v", "ADJ": "a", "ADV": "r"}
WN_LABEL = {"n": "noun", "v": "verb", "a": "adjective", "s": "adjective", "r": "adverb"}
WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'-]{0,39}$")
MAX_CANDIDATES = 8
MAX_SENSES = 3


@lru_cache(maxsize=1)
def _wordnet():
    try:
        import nltk

        if str(NLTK_DIR) not in nltk.data.path:
            nltk.data.path.insert(0, str(NLTK_DIR))
        from nltk.corpus import wordnet

        wordnet.ensure_loaded()
        return wordnet
    except (ImportError, LookupError) as exc:
        logger.warning("WordNet unavailable: %s", exc)
        return None


def _lemma_and_pos(word: str, context: str) -> tuple[str, str | None]:
    nlp = get_nlp()
    if nlp is None:
        return word.lower(), None
    if context:
        for tok in nlp(context):
            if tok.text.lower() == word.lower():
                return tok.lemma_.lower(), POS_TO_WN.get(tok.pos_)
    tok = nlp(word)[0]
    return tok.lemma_.lower(), POS_TO_WN.get(tok.pos_)


def _rank_by_context(synsets, context: str, word: str):
    """Xếp nghĩa theo ngữ cảnh. Điểm = (câu ~ định nghĩa + ví dụ) + (câu ~ câu đã thay từ bằng định nghĩa)
    + chút ưu tiên cho thứ tự WordNet. Thử trên 8 câu: đúng 5, gần đúng 2, sai 1 (colony),
    tốt hơn từng cách riêng lẻ (3/8 và 4/8). Giao diện hiện 3 nghĩa đầu nên nghĩa đúng vẫn thường có mặt.
    """
    if not context or len(synsets) < 2:
        return synsets
    glosses = [f"{s.definition()}. {' '.join(s.examples()[:2])}" for s in synsets]
    pattern = re.compile(rf"{re.escape(word)}", re.IGNORECASE)
    substituted = [pattern.sub(s.definition(), context, count=1) for s in synsets]
    vectors = embed([context] + glosses + substituted)
    if vectors is None:
        return synsets
    n = len(synsets)
    scores = vectors[1:1 + n] @ vectors[0] + vectors[1 + n:] @ vectors[0] - 0.02 * np.arange(n)
    return [synsets[i] for i in np.argsort(-scores)]


def lookup(word: str, context: str = "") -> dict | None:
    word = (word or "").strip().strip("'’")
    if not WORD_RE.match(word):
        return None
    wn = _wordnet()
    if wn is None:
        return None

    lemma, pos = _lemma_and_pos(word, context[:400])
    synsets = []
    for candidate in dict.fromkeys([lemma, word.lower()]):
        synsets = (pos and wn.synsets(candidate, pos=pos)) or wn.synsets(candidate)
        if pos == "a" and not synsets:
            synsets = wn.synsets(candidate, pos="s")
        if synsets:
            lemma = candidate
            break
    if not synsets:
        return None

    ranked = _rank_by_context(synsets[:MAX_CANDIDATES], context, word)
    senses = []
    for s in ranked[:MAX_SENSES]:
        synonyms = [l.name().replace("_", " ") for l in s.lemmas() if l.name().lower() != lemma][:4]
        senses.append({
            "pos": WN_LABEL.get(s.pos(), s.pos()),
            "definition": s.definition(),
            "example": (s.examples() or [""])[0],
            "synonyms": synonyms,
        })
    return {
        "word": word,
        "lemma": lemma,
        "senses": senses,
        "level": word_level(lemma),
        "academic": awl_headword(lemma),
    }
