from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from vocab.models import Word
from writing.models import Submission, WritingPrompt

from .plan import build_today, recommend_prompt
from .weakness import detect_weaknesses, group_of, sentence_around

ESSAY = ("Many people works from home. This have benefits for families. "
         "However, some worker feel lonely at home and they miss there colleagues.")


def agreement(offset, length, fix):
    return {"offset": offset, "length": length, "category": "grammar", "message": "Agreement",
            "replacements": [fix], "rule": "SPACY_SUBJECT_VERB_AGREEMENT"}


class CoachBase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("learner", password="Ielts@2027x")
        self.user.profile.target_band = 7.0
        self.user.profile.daily_minutes = 45
        self.user.profile.save()
        self.p1 = WritingPrompt.objects.create(title="Remote work", prompt_text="Working from home?")
        self.p2 = WritingPrompt.objects.create(title="Technology", prompt_text="Children and phones?")

    def submit(self, prompt=None, essay=ESSAY, words=120, issues=None, features=None, bands=(5.5, 6, 6, 5, 5)):
        overall, tr, cc, lr, gra = bands
        return Submission.objects.create(
            user=self.user, prompt=prompt or self.p1, essay=essay, word_count=words, status="done",
            band_overall=overall, band_task_response=tr, band_coherence=cc, band_lexical=lr, band_grammar=gra,
            issues=issues or [], features={"word_count": words, "complex_sentence_ratio": 0.5,
                                           "linker_variety": 5, "paragraph_count": 4, "awl_ratio": 0.12,
                                           **(features or {})},
        )


class WeaknessTests(CoachBase):
    def test_repeated_agreement_errors_become_top_weakness_with_own_sentences(self):
        issues = [agreement(ESSAY.index("works"), 5, "work"), agreement(ESSAY.index("have"), 4, "has"),
                  agreement(ESSAY.index("feel"), 4, "feels")]
        subs = [self.submit(issues=issues, words=250), self.submit(issues=issues, words=250)]
        top = detect_weaknesses(subs[::-1], target=7.0)[0]
        self.assertEqual(top["key"], "agreement")
        self.assertIn("6 subject-verb agreement errors", top["evidence"])
        example = top["examples"][0]
        self.assertEqual(example["sentence"][example["start"]:example["start"] + example["length"]], "works")
        self.assertEqual(example["fix"], "work")

    def test_short_essays_and_low_academic_vocab_are_detected(self):
        subs = [self.submit(words=150, features={"awl_ratio": 0.03})]
        keys = [w["key"] for w in detect_weaknesses(subs, target=7.0)]
        self.assertIn("length", keys)
        self.assertIn("academic_vocab", keys)

    def test_top_three_cover_different_criteria_first(self):
        issues = [agreement(ESSAY.index("works"), 5, "work")] * 3
        subs = [self.submit(words=150, issues=issues, features={"awl_ratio": 0.02, "complex_sentence_ratio": 0.1})]
        criteria = [w["criterion"] for w in detect_weaknesses(subs, target=7.0)]
        self.assertEqual(len(criteria), len(set(criteria)))

    def test_no_essays_no_weaknesses(self):
        self.assertEqual(detect_weaknesses([], 7.0), [])

    def test_group_of_and_sentence_extraction(self):
        self.assertEqual(group_of({"rule": "EN_A_VS_AN", "category": "grammar"}), "articles")
        self.assertEqual(group_of({"rule": "MORFOLOGIK_RULE_EN_US", "category": "spelling"}), "spelling")
        sentence, start = sentence_around(ESSAY, ESSAY.index("have"), 4)
        self.assertEqual(sentence, "This have benefits for families.")
        self.assertEqual(sentence[start:start + 4], "have")


class PlanTests(CoachBase):
    def test_new_learner_gets_diagnostic_essay_first(self):
        plan = build_today(self.user, [], has_essays=False, days_to_exam=None)
        self.assertEqual(plan["items"][0]["kind"], "diagnostic")

    def test_45_minutes_fits_drill_and_full_essay(self):
        weak = [{"title": "Subject-verb agreement", "examples": [{"sentence": "x"}]}]
        self.submit()
        plan = build_today(self.user, weak, has_essays=True, days_to_exam=None)
        self.assertEqual([i["kind"] for i in plan["items"]], ["drill", "essay"])
        self.assertLessEqual(plan["minutes"], 45)

    def test_short_budget_gets_vocab_and_paragraph(self):
        Word.objects.create(term="mitigate", definition="make less severe")
        self.user.profile.daily_minutes = 30
        self.user.profile.save()
        self.submit()
        plan = build_today(self.user, [], has_essays=True, days_to_exam=None)
        self.assertEqual([i["kind"] for i in plan["items"]], ["vocab", "paragraph"])

    def test_exam_soon_prefers_timed_essay(self):
        Word.objects.create(term="mitigate", definition="make less severe")
        self.submit()
        plan = build_today(self.user, [], has_essays=True, days_to_exam=7)
        self.assertEqual(plan["items"][0]["title"], "Timed essay")

    def test_recommend_untried_then_lowest_band(self):
        self.submit(prompt=self.p1)
        self.assertEqual(recommend_prompt(self.user)["id"], self.p2.id)
        self.submit(prompt=self.p2, bands=(6.5, 6.5, 6.5, 6.5, 6.5))
        rec = recommend_prompt(self.user)
        self.assertEqual(rec["id"], self.p1.id)
        self.assertIn("5.5", rec["reason"])


class TodayApiTests(CoachBase):
    def test_endpoint_requires_login_and_returns_plan(self):
        client = APIClient()
        self.assertEqual(client.get("/api/coach/today/").status_code, 401)
        self.submit(issues=[agreement(ESSAY.index("works"), 5, "work")] * 2, words=200)
        client.force_authenticate(self.user)
        self.user.profile.exam_date = timezone.localdate() + timedelta(days=30)
        self.user.profile.save()
        data = client.get("/api/coach/today/").json()
        self.assertEqual(data["essays_analysed"], 1)
        self.assertTrue(data["weaknesses"])
        self.assertEqual(data["plan"]["budget"], 45)


class ReadingCoachTests(CoachBase):
    def reading_attempt(self, kind_results):
        from reading.models import Attempt, Passage
        passage, _ = Passage.objects.get_or_create(title="Test passage", defaults={"topic": "x", "body": "A.\n\nB."})
        results = [{"number": i + 1, "kind": kind, "correct": ok} for i, (kind, ok) in enumerate(kind_results)]
        return Attempt.objects.create(user=self.user, passage=passage, results=results,
                                      correct=sum(ok for _, ok in kind_results), total=len(kind_results), band=5)

    def test_weak_question_type_becomes_reading_weakness(self):
        attempt = self.reading_attempt([("tfng", False)] * 4 + [("tfng", True)] + [("mcq", True)] * 4)
        weak = detect_weaknesses([], 7.0, reading_attempts=[attempt])
        self.assertEqual([w["key"] for w in weak], ["reading_tfng"])
        self.assertIn("1 of 5 correct", weak[0]["evidence"])
        self.assertEqual(weak[0]["criterion_label"], "Reading")

    def test_too_few_questions_is_not_a_weakness(self):
        attempt = self.reading_attempt([("mcq", False)] * 3)
        self.assertEqual(detect_weaknesses([], 7.0, reading_attempts=[attempt]), [])

    def test_reading_focus_puts_reading_first_in_plan(self):
        from reading.models import Passage
        Passage.objects.create(title="Fresh passage", topic="x", body="A.", minutes=20)
        self.submit()
        focus = [{"title": "True / False / Not Given questions", "criterion": "reading", "examples": []}]
        plan = build_today(self.user, focus, has_essays=True, days_to_exam=None)
        self.assertEqual(plan["items"][0]["kind"], "reading")
        self.assertEqual(plan["items"][0]["passage"]["title"], "Fresh passage")
