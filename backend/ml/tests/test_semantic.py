from unittest import skipUnless

from django.test import SimpleTestCase

from ml.scorer import score_essay
from ml.semantic import CACHE_DIR, semantic_profile

# Không tải model trong test: chỉ chạy khi model đã có sẵn trên máy
HAS_MODEL = CACHE_DIR.exists() and any(CACHE_DIR.rglob("*.onnx"))

PROMPT = ("Some people believe that working from home is more productive than working in an office. "
          "To what extent do you agree or disagree?")
ON_TOPIC = [
    "Working from home has become common, and many people believe it makes employees more productive.",
    "Without a daily commute, remote workers can spend more time on focused tasks and finish projects faster.",
    "However, some employees feel isolated at home and miss the support of colleagues in the office.",
    "In conclusion, I believe a mix of home and office work is the most productive arrangement.",
]
FOOTBALL = ("Football is the most popular sport in the world. Many children dream of playing for famous clubs, "
            "and the World Cup attracts billions of viewers every four years.")
HOLIDAY = ("My favourite holiday was a trip to the beach. I swam in the sea every morning and ate seafood with my family. "
           "The hotel staff were friendly and the weather was perfect.")


@skipUnless(HAS_MODEL, "sentence embedding model not downloaded")
class SemanticTests(SimpleTestCase):
    def test_on_topic_essay_is_relevant(self):
        profile = semantic_profile("\n\n".join(ON_TOPIC), PROMPT)
        self.assertGreater(profile["features"]["semantic_relevance"], 0.4)
        self.assertEqual(profile["detail"]["off_topic_paragraphs"], [])

    def test_drifting_paragraph_is_flagged(self):
        essay = "\n\n".join([ON_TOPIC[0], ON_TOPIC[1], FOOTBALL, ON_TOPIC[3]])
        self.assertEqual(semantic_profile(essay, PROMPT)["detail"]["off_topic_paragraphs"], [3])

    def test_repeated_paragraph_is_redundant(self):
        essay = "\n\n".join([ON_TOPIC[0], ON_TOPIC[1], ON_TOPIC[1], ON_TOPIC[3]])
        self.assertGreater(semantic_profile(essay, PROMPT)["features"]["paragraph_redundancy"], 0.95)

    def test_off_topic_essay_is_capped(self):
        essay = "\n\n".join([HOLIDAY] * 6)
        result = score_essay(essay, PROMPT, "task2")
        self.assertLessEqual(result.task_response, 4.0)
        self.assertLessEqual(result.overall, 4.5)
        self.assertIn("does not seem to answer", result.feedback[0])

    def test_no_prompt_skips_semantic(self):
        self.assertIsNone(semantic_profile("Some text.", ""))
