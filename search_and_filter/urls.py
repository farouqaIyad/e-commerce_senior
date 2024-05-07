from django.urls import path
from .views import SearchList

urlpatterns = [path("search/", SearchList.as_view())]
