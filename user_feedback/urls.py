from django.urls import path
from .views import ReviewList, ReviewDetail

urlpatterns = [
    path("review/", ReviewList.as_view()),
    path("review/<int:pk>/", ReviewDetail.as_view()),
]
