from .views import (
Not
)
from django.urls import path

urlpatterns = [
    path("not/", Not.as_view()),
   
]
