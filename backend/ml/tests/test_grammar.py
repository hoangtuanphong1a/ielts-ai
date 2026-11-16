import json
from unittest import mock

from django.test import SimpleTestCase

from ml.grammar import check_grammar, error_rates, parse_matches
from ml.scorer import score_essay
from ml.tests.test_ml import ESSAY

LT_RESPONSE = {
    "matches": [
        {"offset": 4, "length": 2, "message": "Agreement error", "replacements": [{"value": "goes"}, {"value": "went"}],
         "rule": {"id": "HE_VERB_AGR", "category": {"id": "GRAMMAR"}}},
        {"offset": 31, "length": 5, "message": "Possible spelling mistake", "replacements": [{"value": "bought"}],
         "rule": {"id": "MORFOLOGIK_RULE_EN_US", "category": {"id": "TYPOS"}}},
        {"offset": 10, "length": 1, "message": "Whitespace", "replacements": [],
         "rule": {"id": "WHITESPACE_RULE", "category": {"id": "TYPOGRAPHY"}}},
    ]
}


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class GrammarParseTests(SimpleTestCase):
    def test_parse_maps_categories_and_skips_noise(self):
        issues = parse_matches(LT_RESPONSE["matches"])
        self.assertEqual([i["category"] for i in issues], ["grammar", "spelling"])
        self.assertEqual(issues[0]["replacements"], ["goes", "went"])

    def test_check_grammar_calls_languagetool(self):
        with mock.patch("ml.grammar.urllib.request.urlopen", return_value=FakeResponse(LT_RESPONSE)) as m:
            issues = check_grammar("She go to school.", "http://lt:8010")
        self.assertEqual(len(issues), 2)
        self.assertIn("/v2/check", m.call_args[0][0].full_url)

    def test_unavailable_server_returns_empty(self):
        import urllib.error
        with mock.patch("ml.grammar.urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            self.assertEqual(check_grammar("text", "http://lt:8010"), [])

    def test_no_url_returns_empty(self):
        self.assertEqual(check_grammar("text", None), [])

    def test_error_rates(self):
        issues = parse_matches(LT_RESPONSE["matches"])
        self.assertEqual(error_rates(issues, 100), {"grammar_per_100": 1.0, "spelling_per_100": 1.0})


class GrammarScoringTests(SimpleTestCase):
    def test_many_grammar_errors_lower_grammar_band(self):
        text = "\n\n".join([ESSAY] * 4)
        clean = score_essay(text, "working from home productive", "task2")
        errors = [{"category": "grammar", "offset": 0, "length": 1, "message": "", "replacements": [], "rule": ""}] * 20
        messy = score_essay(text, "working from home productive", "task2", grammar_issues=errors)
        self.assertLess(messy.grammar, clean.grammar)
        self.assertTrue(any("grammar" in tip.lower() for tip in messy.feedback))

    def test_no_issues_keeps_scores(self):
        text = "\n\n".join([ESSAY] * 4)
        a = score_essay(text, "", "task2")
        b = score_essay(text, "", "task2", grammar_issues=[])
        self.assertEqual(a.grammar, b.grammar)


class SpellingVariantTests(SimpleTestCase):
    def match(self, word, replacement):
        return {"offset": 0, "length": len(word), "message": "", "replacements": [{"value": replacement}],
                "context": {"text": f"{word} here", "offset": 0, "length": len(word)},
                "rule": {"id": "MORFOLOGIK_RULE_EN_US", "category": {"id": "TYPOS"}}}

    def test_british_spellings_are_not_errors(self):
        for uk, us in [("emphasise", "emphasize"), ("organisational", "organizational"),
                       ("colour", "color"), ("centre", "center"), ("travelled", "traveled")]:
            self.assertEqual(parse_matches([self.match(uk, us)]), [], uk)

    def test_real_misspellings_are_kept(self):
        self.assertEqual(len(parse_matches([self.match("recieve", "receive"), self.match("employes", "employs")])), 2)
