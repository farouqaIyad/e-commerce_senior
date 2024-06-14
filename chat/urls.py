from django .urls import path

urlpatterns = [
    path(''),
    path("<str:room_name>/")
]