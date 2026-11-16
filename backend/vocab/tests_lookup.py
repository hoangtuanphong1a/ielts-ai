from unittest import skipUnless

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from ml.dictionary import _wordnet, lookup

from .models import Card, Word

HAS_WORDNET = _wordnet() is not None
CONTEXT = "Hundreds of species of wild bees, many of them solitary, depend on the same flowers."


@skipUnless(HAS_WORDNET, "WordNet data not downloaded")
class DictionaryTests(TestCase):
    def test_lemma_level_and_context_sense(self):
        result = lookup("solitary", CONTEXT)
        self.assertEqual(result["lemma"], "solitary")
        self.assertIn("plants and animals", result["senses"][0]["definition"])
        self.assertEqual(result["level"], "advanced")

    def test_inflected_form_and_awl(self):
        result = lookup("analysing")
        self.assertEqual(result["lemma"], "analyse")
        self.assertEqual(result["academic"], "analyse")

    def test_unknown_or_invalid_word(self):
        self.assertIsNone(lookup("xqzt"))
        self.assertIsNone(lookup("two words"))
        self.assertIsNone(lookup("<script>"))


class AddCardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("reader", password="Ielts@2027x")
        self.other = get_user_model().objects.create_user("other", password="Ielts@2027x")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def add(self, term="solitary"):
        return self.client.post("/api/vocab/cards/add/", {
            "term": term, "definition": "not living in groups", "context": CONTEXT,
            "source": "Reading: The Rise of Urban Beekeeping"}, format="json")

    def test_add_creates_card_with_context_once(self):
        first, second = self.add(), self.add()
        self.assertEqual((first.status_code, second.status_code), (201, 200))
        card = Card.objects.get(user=self.user)
        self.assertEqual(card.context, CONTEXT)
        self.assertEqual(card.word.added_by, self.user)

    def test_added_word_is_not_given_to_other_learners_as_new(self):
        self.add()
        Word.objects.create(term="mitigate", definition="make less severe")
        client = APIClient()
        client.force_authenticate(self.other)
        terms = [c["word"]["term"] for c in client.get("/api/vocab/cards/due/").json()]
        self.assertEqual(terms, ["mitigate"])

    def test_existing_curated_word_is_reused(self):
        Word.objects.create(term="mitigate", definition="make less severe")
        self.add("Mitigate")
        self.assertEqual(Word.objects.filter(term__iexact="mitigate").count(), 1)
        self.assertIsNone(Word.objects.get(term="mitigate").added_by)

    @skipUnless(HAS_WORDNET, "WordNet data not downloaded")
    def test_lookup_endpoint_reports_in_deck(self):
        res = self.client.get("/api/vocab/lookup/", {"word": "solitary", "context": CONTEXT})
        self.assertFalse(res.json()["in_deck"])
        self.add()
        self.assertTrue(self.client.get("/api/vocab/lookup/", {"word": "solitary"}).json()["in_deck"])
        self.assertEqual(self.client.get("/api/vocab/lookup/", {"word": "xqzt"}).status_code, 404)
