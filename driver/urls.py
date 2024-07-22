from django.urls import path

from . import views

urlpatterns = [
    path("", views.DriverList.as_view()),
    path("detail", views.DriverDetail.as_view()),
    path("approve", views.ApproveDriver.as_view()),
    path("all", views.AdminViewDriver.as_view()),
]
