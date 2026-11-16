from django.test import SimpleTestCase

from ml.features import extract_features, tokenize
from ml.scorer import round_band, score_essay
from vocab.srs import sm2

ESSAY = (
    "Some people believe that working from home is more productive. "
    "However, others argue that offices encourage collaboration.\n\n"
    "Firstly, remote work removes commuting, which saves time. "
    "Moreover, employees can organise their schedules flexibly.\n\n"
    "Nevertheless, isolation can reduce motivation because colleagues are absent. "
    "Consequently, some workers become less productive.\n\n"
    "In conclusion, although working from home has clear advantages, "
    "a hybrid model is likely the most effective solution."
)


class FeatureTests(SimpleTestCase):
    def test_tokenize_lowercases_and_keeps_apostrophes(self):
        self.assertEqual(tokenize("Children's Toys"), ["children's", "toys"])

    def test_extract_counts(self):
        f = extract_features(ESSAY, "Is working from home more productive?")
        self.assertEqual(f["paragraph_count"], 4)
        self.assertGreater(f["linker_variety"], 3)
        self.assertGreater(f["prompt_overlap"], 0.5)

    def test_empty_text_does_not_crash(self):
        f = extract_features("")
        self.assertEqual(f["word_count"], 0)


class ScorerTests(SimpleTestCase):
    def test_round_band(self):
        self.assertEqual(round_band(6.25), 6.5)
        self.assertEqual(round_band(6.75), 7.0)
        self.assertEqual(round_band(6.1), 6.0)
        self.assertEqual(round_band(12), 9.0)

    def test_short_essay_is_capped(self):
        # ESSAY = 65 từ, Task 2 cần 250: không được band cao dù câu chữ tốt
        r = score_essay(ESSAY, "working from home productive", "task2")
        self.assertLessEqual(r.overall, 5.5)
        self.assertLessEqual(r.task_response, 5.5)

    def test_long_enough_essay_not_capped(self):
        long = "\n\n".join([ESSAY] * 4)  # 260 từ
        r = score_essay(long, "working from home productive", "task2")
        self.assertGreater(r.overall, 5.5)

    def test_score_in_range(self):
        r = score_essay(ESSAY, "working from home productive", "task2")
        self.assertEqual(r.scorer, "heuristic")
        self.assertTrue(4 <= r.overall <= 9)
        self.assertTrue(r.feedback)


class SM2Tests(SimpleTestCase):
    def test_correct_answers_grow_interval(self):
        reps, interval, ease = sm2(5, 0, 0, 2.5)
        self.assertEqual((reps, interval), (1, 1))
        reps, interval, ease = sm2(5, reps, interval, ease)
        self.assertEqual(interval, 6)
        reps, interval, ease = sm2(5, reps, interval, ease)
        self.assertGreater(interval, 6)

    def test_wrong_answer_resets(self):
        reps, interval, ease = sm2(1, 5, 30, 2.5)
        self.assertEqual((reps, interval), (0, 1))
        self.assertGreaterEqual(ease, 1.3)
