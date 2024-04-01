from django.urls import path
from .views import add_review,add_complaint

urlpatterns = [
    path('review/add/', add_review),
    path('complaint/add/', add_complaint),
]