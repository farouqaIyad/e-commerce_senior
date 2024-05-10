from django.urls import path
from .views import SearchProduct

urlpatterns = [path("search/<str:query>", SearchProduct.as_view())]
