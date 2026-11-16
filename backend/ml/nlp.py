"""Nạp spaCy một lần, dùng chung cho các bộ phân tích (agreement, lexical).

spaCy hoặc model chưa cài -> get_nlp() trả None, các bộ phân tích tự bỏ qua.
"""
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

SPACY_MODEL = "en_core_web_sm"


@lru_cache(maxsize=1)
def get_nlp():
    try:
        import spacy

        return spacy.load(SPACY_MODEL, disable=["ner"])
    except (ImportError, OSError) as exc:
        logger.warning("spaCy model %s unavailable: %s", SPACY_MODEL, exc)
        return None
