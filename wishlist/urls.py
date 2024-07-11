from .views import WishlistList
from django.urls import path

urlpatterns = [
    path("wishlist/", WishlistList.as_view()),
]
