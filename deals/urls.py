from .views import DealsList
from django.urls import path

urlpatterns = [
    path("deals/", DealsList.as_view()),
]
