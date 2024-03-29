from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import signup,login,delete_account
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signup),
    path('login/', login),
    path('show/', delete_account),

    
]