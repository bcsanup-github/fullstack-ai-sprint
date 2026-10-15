import os 
import requests
from django.core.cache import cache
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()


MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
client = InferenceClient(api_key=os.getenv("HF_TOKEN"), provider="auto")

def get_ai_summary(city, temp, description):
    if MOCK_MODE:
        return f"[MOCK] Its {temp}°C and {description} in {city} - grab a light jacket!"
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen3-32B",
            max_token=100,
            temperature=0.5,
            message=[
                {"role": "system", "content": "you write one short, friendly weather sentence."},
                {"role": "user", "content": f"weather in {city}: {temp}°C, {description}."},
            ],
        )
        return completion.choices[0].message.content
    except HfHubHTTPError:
        return "AI summary unavaiable right now."

class WeatherView(APIView):
    def get(self, request):
        city = request.query_params.get("city", "").strip()
        if not city:
            return Response({"error": "city is required"}, status=400)

        cache_key = f"weather:{city.lower()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        if MOCK_MODE:
            weather = {"city": city, "temp": 18, "description": "partly cloudy", "humidity": 65}
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
            res = requests.get(url, params=params, timeout=10)
            if res.status_code != 200:
                return Response({"error": "city not found"}, status=404)
            data = res.json()
            weather = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
            }

        weather["ai_summary"] = get_ai_summary(
            weather["city"], weather["temp"], weather["description"]
        )

        cache.set(cache_key, weather, timeout=600)
        return Response(weather)