"""Đặc trưng ngữ nghĩa bằng Sentence-BERT (T2.4, WRI-13).

Model: sentence-transformers/all-MiniLM-L6-v2 chạy bằng ONNX qua fastembed (không cần PyTorch).
Model tải về một lần (~90MB) vào ml/artifacts/embeddings, bài viết không gửi ra ngoài.

Đo thực tế cho thấy:
- Độ tương đồng bài - đề tách rõ bài đúng đề (~0.6) và lạc đề (~0), nhưng KHÔNG phản ánh chất
  lượng (bài yếu lặp lại từ trong đề còn cao hơn). -> chỉ dùng để phạt lạc đề, chỉ ra đoạn lạc đề.
- Độ tương đồng câu liền kề KHÔNG phát hiện được câu bị xáo trộn thứ tự, nên không gọi là
  "mạch lạc". Nó chỉ đo các câu có cùng chủ đề hay không -> "topic_continuity", trọng số thấp.
- Hai đoạn gần như trùng nhau (lặp ý / chép lại) -> "paragraph_redundancy" cao.

fastembed chưa cài, model không tải được, hoặc IELTS_SEMANTIC=0 -> trả None.
"""
import logging
import os
from functools import lru_cache
from pathlib import Path

import numpy as np

from .features import split_paragraphs, split_sentences

logger = logging.getLogger(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CACHE_DIR = Path(__file__).parent / "artifacts" / "embeddings"
OFF_TOPIC = 0.2  # đoạn có độ tương đồng với đề dưới ngưỡng này -> có thể lạc đề


@lru_cache(maxsize=1)
def get_model():
    if os.environ.get("IELTS_SEMANTIC", "1") == "0":
        return None
    try:
        from fastembed import TextEmbedding

        return TextEmbedding(MODEL_NAME, cache_dir=str(CACHE_DIR))
    except Exception as exc:  # noqa: BLE001 - thiếu thư viện / không tải được model: bỏ qua
        logger.warning("Sentence embedding model unavailable: %s", exc)
        return None


def embed(texts: list[str]) -> np.ndarray | None:
    model = get_model()
    if model is None:
        return None
    vectors = np.array(list(model.embed(texts)), dtype=np.float32)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True).clip(min=1e-9)


def semantic_profile(essay: str, prompt: str) -> dict | None:
    paragraphs = split_paragraphs(essay)
    sentences = split_sentences(essay)
    if not prompt.strip() or not paragraphs or not sentences:
        return None
    vectors = embed([prompt, essay] + paragraphs + sentences)
    if vectors is None:
        return None

    p_vec, e_vec = vectors[0], vectors[1]
    para_vecs = vectors[2:2 + len(paragraphs)]
    sent_vecs = vectors[2 + len(paragraphs):]

    para_relevance = [float(p_vec @ v) for v in para_vecs]
    continuity = (
        float(np.mean([sent_vecs[i] @ sent_vecs[i + 1] for i in range(len(sent_vecs) - 1)]))
        if len(sent_vecs) > 1 else 0.0
    )
    redundancy = 0.0
    if len(para_vecs) > 1:
        sims = para_vecs @ para_vecs.T
        np.fill_diagonal(sims, -1)
        redundancy = float(sims.max())

    return {
        "features": {
            "semantic_relevance": float(p_vec @ e_vec),
            "topic_continuity": continuity,
            "paragraph_redundancy": redundancy,
        },
        "detail": {
            "paragraph_relevance": [round(r, 3) for r in para_relevance],
            "off_topic_paragraphs": [i + 1 for i, r in enumerate(para_relevance) if r < OFF_TOPIC],
        },
    }
