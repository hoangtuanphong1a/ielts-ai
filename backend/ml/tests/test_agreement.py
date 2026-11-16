import importlib.util
from unittest import skipUnless

from django.test import SimpleTestCase

from ml.agreement import check_agreement, merge_issues
from ml.grammar import parse_matches

HAS_SPACY = importlib.util.find_spec("spacy") is not None and importlib.util.find_spec("en_core_web_sm") is not None


@skipUnless(HAS_SPACY, "spaCy model en_core_web_sm not installed")
class AgreementTests(SimpleTestCase):
    def fixes(self, text):
        return {text[i["offset"]:i["offset"] + i["length"]]: i["replacements"][0] for i in check_agreement(text)}

    def test_catches_common_learner_errors(self):
        text = ("Many people works from home and this have benefits. "
                "Working from home are productive. They saves money. My brother go to school. "
                "The students was tired. Everyone want a good job.")
        self.assertEqual(self.fixes(text), {
            "works": "work", "have": "has", "are": "is", "saves": "save",
            "go": "goes", "was": "were", "want": "wants",
        })

    def test_no_false_positives_on_correct_sentences(self):
        text = ("The number of students who study abroad is rising. One of the reasons is cost. "
                "Some of the workers are happy. Teachers and parents agree. People who live alone feel lonely. "
                "What matters is effort. He has a car and she does too. I am sure that it works. "
                "I suggest that he go home. Go to bed early. Children should play outside.")
        self.assertEqual(check_agreement(text), [])

    def test_keeps_capital_letter(self):
        self.assertEqual(self.fixes("They was late. Is the children ready?").get("was"), "were")


class MergeTests(SimpleTestCase):
    def test_overlapping_issue_is_dropped(self):
        lt = [{"offset": 5, "length": 4, "category": "grammar"}]
        extra = [{"offset": 6, "length": 2, "category": "grammar"}, {"offset": 20, "length": 3, "category": "grammar"}]
        self.assertEqual([i["offset"] for i in merge_issues(lt, extra)], [5, 20])


class CategoryTests(SimpleTestCase):
    def test_a_vs_an_is_grammar_and_confused_words_is_spelling(self):
        issues = parse_matches([
            {"offset": 0, "length": 1, "message": "", "replacements": [], "rule": {"id": "EN_A_VS_AN", "category": {"id": "MISC"}}},
            {"offset": 5, "length": 5, "message": "", "replacements": [], "rule": {"id": "THERE_THEIR", "category": {"id": "CONFUSED_WORDS"}}},
        ])
        self.assertEqual([i["category"] for i in issues], ["grammar", "spelling"])
