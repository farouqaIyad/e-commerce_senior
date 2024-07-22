from .views import (
    notificationList,
)
from django.urls import path

urlpatterns = [
    path("notification/", notificationList.as_view()),
]
