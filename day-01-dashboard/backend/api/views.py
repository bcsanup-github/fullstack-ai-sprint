from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime


def ping(request):
    return JsonResponse({"status": "ok"})


class MetricsView(APIView):
    def get(self, request):
        metrics = [
            {"name": "Revenue", "value": 4200, "trend": "up"},
            {"name": "Users",   "value": 180,  "trend": "up"},
            {"name": "Errors",  "value": 3,    "trend": "down"},
            {"name": "Uptime",  "value": 99,   "trend": "flat"},
        ]
        return Response(metrics)

class TimeView(APIView):
    def get(self, request):
        return Response({"time": datetime.now().isoformat()})