import json
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PromptSerializer

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
client = InferenceClient(api_key=os.getenv("HF_TOKEN"), provider="auto")

SYSTEM_PROMPTS = {
    "summarize": "You are a concise summarizer. Reply in 1-2 clear sentences.",
    "rewrite": "You rewrite the user's text to be clearer and more polished.",
    "explain": "You explain the user's text simply, as if to a curious beginner.",
    "analyze": (
        "Analyze the user's text. Respond with ONLY valid JSON, no other text, "
        'in this exact shape: '
        '{"sentiment": "positive|negative|neutral", '
        '"topics": ["topic1", "topic2"], '
        '"summary": "one sentence"}'
    ),
}


def parse_json_reply(reply):
    cleaned = reply.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "Model did not return valid JSON", "raw": reply}


class PromptView(APIView):
    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # --- MOCK PATH: return a fake reply, no API call, no credits ---
        if MOCK_MODE:
            if data["mode"] == "analyze":
                return Response({
                    "reply": {
                        "sentiment": "positive",
                        "topics": ["mock", "demo"],
                        "summary": f"Mock analysis of: {data['prompt'][:40]}",
                    },
                    "tokens": 0,
                    "mock": True,
                })
            return Response({
                "reply": f"[MOCK · {data['mode']}] You sent: {data['prompt']}",
                "tokens": 0,
                "mock": True,
            })

        # --- REAL PATH: only runs when MOCK_MODE is False ---
        try:
            completion = client.chat.completions.create(
                model="Qwen/Qwen3-32B",
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[data["mode"]]},
                    {"role": "user", "content": data["prompt"]},
                ],
            )
            reply_text = completion.choices[0].message.content
            reply = parse_json_reply(reply_text) if data["mode"] == "analyze" else reply_text
            return Response({
                "reply": reply,
                "tokens": completion.usage.total_tokens,
                "mock": False,
            })
        except HfHubHTTPError:
            return Response(
                {"error": "AI service unavailable right now. Try again later."},
                status=503,
            )