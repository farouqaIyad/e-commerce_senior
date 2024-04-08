from .views import admin_signup ,customer_signup, supplier_signup, driver_signup, customersupporter_signup,login,delete_account
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/signup/', admin_signup),
    path('customer/signup/', customer_signup),
    path('supplier/signup/', supplier_signup),
    path('driver/signup/', driver_signup),
    path('customersupporter/signup/', customersupporter_signup),
    path('login/', login),
    path('delete/', delete_account),
]