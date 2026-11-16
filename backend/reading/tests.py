from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from .content import PASSAGES
from .grading import band_from_score, is_correct
from .models import Passage


class GradingTests(SimpleTestCase):
    def test_tfng_accepts_case_and_short_forms(self):
        self.assertTrue(is_correct("tfng", ["NOT GIVEN"], "not given"))
        self.assertTrue(is_correct("tfng", ["NOT GIVEN"], "NG"))
        self.assertTrue(is_correct("tfng", ["TRUE"], "t"))
        self.assertFalse(is_correct("tfng", ["TRUE"], "FALSE"))
        self.assertTrue(is_correct("ynng", ["NO"], "n"))

    def test_completion_ignores_case_punctuation_and_leading_article(self):
        self.assertTrue(is_correct("completion", ["bus shelters"], "  Bus Shelters. ", 2))
        self.assertTrue(is_correct("completion", ["varroa mite"], "the varroa mite", 3))
        self.assertFalse(is_correct("completion", ["varroa mite"], "the varroa mite", 2))  # 3 từ > giới hạn 2, như thi thật
        self.assertTrue(is_correct("completion", ["wild species", "wild bees"], "wild bees", 2))

    def test_completion_over_word_limit_is_wrong(self):
        self.assertFalse(is_correct("completion", ["bus shelters"], "the roofs of bus shelters", 2))

    def test_blank_is_wrong(self):
        self.assertFalse(is_correct("mcq", ["B"], ""))

    def test_band_conversion_scales_to_40(self):
        self.assertEqual(band_from_score(12, 12), 9.0)
        self.assertEqual(band_from_score(9, 12), 7.0)   # 30/40
        self.assertEqual(band_from_score(6, 12), 5.5)   # 20/40 -> 5.5
        self.assertEqual(band_from_score(0, 12), 0.0)

    def test_every_evidence_quote_is_in_its_passage(self):
        for passage in PASSAGES:
            for group in passage["groups"]:
                for q in group["questions"]:
                    self.assertIn(q[4], passage["body"], f"{passage['title']} Q{q[0]}")


class ReadingApiTests(TestCase):
    def setUp(self):
        call_command("seed_reading", stdout=open("nul" if __import__("os").name == "nt" else "/dev/null", "w"))
        self.user = get_user_model().objects.create_user("reader", password="Ielts@2027x")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.passage = Passage.objects.get(title="The Rise of Urban Beekeeping")

    def test_detail_hides_answers(self):
        data = self.client.get(f"/api/reading/passages/{self.passage.id}/").json()
        question = data["groups"][0]["questions"][0]
        self.assertNotIn("answers", question)
        self.assertNotIn("explanation", question)
        self.assertEqual(sum(len(g["questions"]) for g in data["groups"]), 12)

    def test_submit_grades_and_returns_explanations(self):
        answers = {"1": "TRUE", "2": "FALSE", "3": "TRUE", "4": "NOT GIVEN", "6": "E", "10": "wild bees", "12": "bus shelters"}
        res = self.client.post(f"/api/reading/passages/{self.passage.id}/attempts/",
                               {"answers": answers, "duration_seconds": 600}, format="json")
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual((data["correct"], data["total"]), (6, 12))
        q3 = next(r for r in data["results"] if r["number"] == 3)
        self.assertFalse(q3["correct"])
        self.assertEqual(q3["answer"], "FALSE")
        self.assertIn(q3["evidence"], self.passage.body)

    def test_list_shows_my_best_band_only(self):
        other = get_user_model().objects.create_user("other", password="Ielts@2027x")
        self.passage.attempts.create(user=other, band=9.0, correct=12, total=12)
        self.passage.attempts.create(user=self.user, band=5.5, correct=7, total=12)
        rows = {p["title"]: p for p in self.client.get("/api/reading/passages/").json()}
        self.assertEqual(rows[self.passage.title]["best_band"], 5.5)
        self.assertEqual(rows[self.passage.title]["attempt_count"], 1)
        self.assertEqual(rows[self.passage.title]["question_count"], 12)

    def test_cannot_read_other_users_attempt(self):
        other = get_user_model().objects.create_user("other2", password="Ielts@2027x")
        attempt = self.passage.attempts.create(user=other, band=6, correct=8, total=12)
        self.assertEqual(self.client.get(f"/api/reading/attempts/{attempt.id}/").status_code, 404)
