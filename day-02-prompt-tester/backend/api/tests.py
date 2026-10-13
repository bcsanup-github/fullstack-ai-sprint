from rest_framework.test import APITestCase


class PromptEndpointTests(APITestCase):
    def test_valid_prompt_returns_200(self):
        res = self.client.post(
            "/api/prompt/",
            {"prompt": "hello", "mode": "summarize"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("reply", res.data)

    def test_empty_prompt_returns_400(self):
        res = self.client.post("/api/prompt/", {"prompt": ""}, format="json")
        self.assertEqual(res.status_code, 400)

    def test_invalid_mode_returns_400(self):
        res = self.client.post(
            "/api/prompt/",
            {"prompt": "hi", "mode": "nonsense"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)