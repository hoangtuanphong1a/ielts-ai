import importlib.util
from unittest import skipUnless

from django.test import SimpleTestCase

from ml.lexical import awl, awl_headword, lexical_profile
from ml.scorer import score_essay

HAS_NLP = all(importlib.util.find_spec(m) for m in ("spacy", "en_core_web_sm", "wordfreq"))

WEAK = ("Nowadays many people work from home. I think it is good because they do not go to office. "
        "They can stay with family and they are happy. But some people do not like it because they are alone. "
        "They want to see friends at work. So working from home is good and bad.")
STRONG = ("The shift towards remote employment has generated considerable debate regarding its impact on productivity. "
          "Proponents argue that eliminating the daily commute enables employees to allocate more time to focused tasks, "
          "thereby enhancing output. Nevertheless, critics emphasise that the absence of face-to-face interaction can "
          "undermine collaboration and erode organisational culture.")


class AwlTests(SimpleTestCase):
    def test_list_has_570_headwords_in_10_sublists(self):
        data = awl()
        self.assertEqual(len(data), 570)
        self.assertEqual(sorted(set(data.values())), list(range(1, 11)))

    def test_derived_and_american_forms_map_to_headword(self):
        self.assertEqual(awl_headword("analysis"), "analyse")
        self.assertEqual(awl_headword("analyze"), "analyse")
        self.assertEqual(awl_headword("significance"), "significant")
        self.assertEqual(awl_headword("economic"), "economy")
        self.assertEqual(awl_headword("labor"), "labour")

    def test_unrelated_words_do_not_match(self):
        for word in ["creature", "surveillance", "house", "happy"]:
            self.assertIsNone(awl_headword(word), word)


@skipUnless(HAS_NLP, "spaCy / wordfreq not installed")
class LexicalProfileTests(SimpleTestCase):
    def test_strong_essay_uses_more_academic_and_less_common_words(self):
        weak, strong = lexical_profile(WEAK)["features"], lexical_profile(STRONG)["features"]
        self.assertGreater(strong["awl_ratio"], weak["awl_ratio"] + 0.2)
        self.assertGreater(strong["advanced_ratio"], weak["advanced_ratio"])

    def test_profile_lists_words_for_the_ui(self):
        profile = lexical_profile(STRONG)["profile"]
        self.assertIn("generate", profile["academic_words"])
        self.assertEqual(set(profile["levels"]), {"basic", "intermediate", "advanced"})

    def test_lexical_band_rewards_richer_vocabulary(self):
        weak = score_essay(WEAK * 3, "working from home", "task2")
        strong = score_essay(STRONG * 3, "working from home", "task2")
        self.assertGreater(strong.lexical, weak.lexical)
        self.assertIn("vocab", strong.features)
        self.assertTrue(any("academic vocabulary" in tip for tip in weak.feedback))
