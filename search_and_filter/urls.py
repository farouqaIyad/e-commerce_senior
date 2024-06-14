from django.urls import path
from .views import SearchProduct, completion

urlpatterns = [
    path("search/<str:query>", SearchProduct.as_view()),
    path("completion/<str:query>", completion.as_view()),
    # path("change", change_embedding.as_view())
]
