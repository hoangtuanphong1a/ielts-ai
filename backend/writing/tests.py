from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from vocab.models import Word
from writing.models import WritingPrompt

ESSAY = (
    "Some people believe that working from home is more productive. However, "
    "others argue that offices encourage collaboration and teamwork among staff.\n\n"
    "Firstly, remote work removes commuting, which saves a great deal of time."
)


class ApiFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("learner", password="S3cure-pass!")
        self.other = User.objects.create_user("other", password="S3cure-pass!")
        self.prompt = WritingPrompt.objects.create(
            title="Remote work", prompt_text="Is working from home more productive?"
        )
        Word.objects.create(term="mitigate", definition="make less severe")

    def login(self, username="learner"):
        res = self.client.post("/api/auth/token/",
                               {"username": username, "password": "S3cure-pass!"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def test_requires_auth(self):
        res = self.client.get("/api/writing/prompts/")
        self.assertEqual(res.status_code, 401)

    def test_submit_essay_is_scored_and_private(self):
        self.login()
        res = self.client.post("/api/writing/submissions/",
                               {"prompt": self.prompt.id, "essay": ESSAY})
        self.assertEqual(res.status_code, 201, res.data)
        self.assertGreater(res.data["band_overall"], 0)
        self.assertTrue(res.data["feedback"])

        progress = self.client.get("/api/writing/progress/").data
        self.assertEqual(progress["count"], 1)

        self.login("other")
        self.assertEqual(len(self.client.get("/api/writing/submissions/").data), 0)

    def test_vocab_due_and_review(self):
        self.login()
        cards = self.client.get("/api/vocab/cards/due/").data
        self.assertEqual(len(cards), 1)
        res = self.client.post(f"/api/vocab/cards/{cards[0]['id']}/review/", {"quality": 5})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["repetitions"], 1)
        # đã ôn, hạn ngày mai -> hôm nay không còn thẻ
        self.assertEqual(len(self.client.get("/api/vocab/cards/due/").data), 0)
