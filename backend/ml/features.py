"""Trích xuất đặc trưng NLP từ bài luận IELTS Writing.

Không phụ thuộc thư viện NLP nặng (spaCy/NLTK) — chỉ dùng regex,
để dễ đọc và dễ tự gõ lại.
"""
import math
import re
from collections import Counter

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n")

# Từ nối (Coherence & Cohesion)
LINKERS = {
    "however", "moreover", "furthermore", "therefore", "consequently",
    "nevertheless", "nonetheless", "additionally", "firstly", "secondly",
    "finally", "overall", "conversely", "similarly", "likewise", "meanwhile",
    "hence", "thus", "although", "whereas", "while", "despite", "because",
    "since", "instance", "example", "conclusion", "addition", "contrast",
}

# Từ nối mệnh đề phụ -> câu phức (Grammatical Range)
SUBORDINATORS = {
    "although", "because", "since", "unless", "whereas", "while", "if",
    "when", "which", "who", "whom", "whose", "that", "though", "until",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for",
    "with", "is", "are", "was", "were", "be", "been", "it", "this", "that",
    "as", "at", "by", "from", "they", "their", "there", "can", "will",
    "would", "should", "not", "i", "we", "you", "he", "she", "his", "her",
    "our", "my", "more", "than", "so", "do", "does", "have", "has", "had",
}

FEATURE_NAMES = [
    "word_count",
    "sentence_count",
    "paragraph_count",
    "avg_sentence_len",
    "guiraud_index",       # đa dạng từ vựng = unique / sqrt(total)
    "long_word_ratio",     # tỉ lệ từ >= 7 ký tự
    "linker_count",
    "linker_variety",
    "complex_sentence_ratio",
    "top_word_repeat_ratio",
    "prompt_overlap",
]


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in PARAGRAPH_SPLIT_RE.split(text.strip()) if p.strip()]


def extract_features(text: str, prompt: str = "") -> dict[str, float]:
    words = tokenize(text)
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)

    n_words = len(words)
    n_sent = max(len(sentences), 1)
    content_words = [w for w in words if w not in STOPWORDS]

    linkers_used = [w for w in words if w in LINKERS]
    complex_sents = sum(
        1 for s in sentences if any(w in SUBORDINATORS for w in tokenize(s))
    )

    counts = Counter(content_words)
    top_repeat = counts.most_common(1)[0][1] if counts else 0

    prompt_keywords = {w for w in tokenize(prompt) if w not in STOPWORDS and len(w) > 3}
    overlap = (
        len(prompt_keywords & set(content_words)) / len(prompt_keywords)
        if prompt_keywords
        else 0.0
    )

    return {
        "word_count": float(n_words),
        "sentence_count": float(len(sentences)),
        "paragraph_count": float(len(paragraphs)),
        "avg_sentence_len": n_words / n_sent,
        "guiraud_index": len(set(words)) / math.sqrt(n_words) if n_words else 0.0,
        "long_word_ratio": sum(1 for w in words if len(w) >= 7) / n_words if n_words else 0.0,
        "linker_count": float(len(linkers_used)),
        "linker_variety": float(len(set(linkers_used))),
        "complex_sentence_ratio": complex_sents / n_sent,
        "top_word_repeat_ratio": top_repeat / len(content_words) if content_words else 0.0,
        "prompt_overlap": overlap,
    }


def features_to_vector(feats: dict[str, float]) -> list[float]:
    return [feats[name] for name in FEATURE_NAMES]


class HandcraftedFeatures(BaseEstimator, TransformerMixin):
    """Transformer sklearn: list[str] -> ma trận đặc trưng thủ công."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([features_to_vector(extract_features(t)) for t in X])
    