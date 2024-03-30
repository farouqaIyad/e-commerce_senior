from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import customer_signup,admin_signup,login,delete_account
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', customer_signup),
    path('admin/signup/', admin_signup),
    path('login/', login),
    path('show/', delete_account),

    
]