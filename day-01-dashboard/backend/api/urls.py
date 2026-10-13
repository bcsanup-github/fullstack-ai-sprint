from django.urls import path

from .views import MetricsView, TimeView, ping

urlpatterns = [
    path("ping/", ping),
    path("metrics/", MetricsView.as_view()),
    path("time/",  TimeView.as_view())
]