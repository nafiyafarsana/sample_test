from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, VendorPerformanceView
from .views import MyTokenObtainPairView, MyTokenRefreshView


router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_order')
router.register(r'vendor_performance', VendorPerformanceView, basename='vendor_performance')
urlpatterns = router.urls

urlpatterns = router.urls + [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view({'get': 'get'}), name='vendor-performance'),
    path('purchase_orders/<str:pk>/acknowledge/', PurchaseOrderViewSet.as_view({'post': 'acknowledge'}), name='acknowledge-purchase-order'),

    ]