from django.urls import path
from .views import (
    SearchProduct,
    completion,
    change_embedding,
    FiltersList,
    supplierSearchProduct,
    Highest_rating,
    bestsellers,
    Newly_added,
)

urlpatterns = [
    path("search/<str:query>", SearchProduct.as_view()),
    path("supplier/search/<str:query>", supplierSearchProduct.as_view()),
    path("completion/", completion.as_view()),
    path("filters/", FiltersList.as_view()),
    path("change", change_embedding.as_view()),
    path("highest_rating", Highest_rating.as_view()),
    path("newly_added", Newly_added.as_view()),
]
