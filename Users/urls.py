from django.urls import path
from .views import AdminList,AdminDetail,CustomerList,CustomerDetail,SupplierList,SupplierDetail\
    ,CustomerSupporterList,CustomerSupporterDetail,DriverList,DriverDetail
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/',AdminList.as_view()),
    path('admin/<str:pk>',AdminDetail.as_view()),
    path('customer/',CustomerList.as_view()),
    path('customer/<str:pk>',CustomerDetail.as_view()),
    path('supplier/',SupplierList.as_view()),
    path('supplier/<str:pk>',SupplierDetail.as_view()),
    path('driver',DriverList.as_view()),
    path('driver/<str:pk>',DriverDetail.as_view()),
    path('customersupporter/',CustomerSupporterList.as_view()),
    path('customersupporter/<str:pk>',CustomerSupporterDetail.as_view()),
]