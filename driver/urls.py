from django.urls import path

from . import views

urlpatterns = [
    path("", views.DriverList.as_view()),
    path("<int:pk>", views.DriverDetail.as_view()),
]
