from django.urls import path
from .views import registerUser,deleteUser,view_something
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('signup/', registerUser, name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete/',deleteUser),
    path('view/',view_something)


]