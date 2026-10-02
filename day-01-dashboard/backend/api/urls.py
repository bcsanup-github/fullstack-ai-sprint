from django.urls import path
from .views import ping, MetricsView, TimeView

urlpatterns = [
    path("ping/", ping),
    path("metrics/", MetricsView.as_view()),
    path("time/",  TimeView.as_view())
]