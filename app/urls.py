# urls.py
from django.urls import path
from .views import *
# from rest_framework.authtoken import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("api/vendors/", vendors, name='vendors'),
    path("api/vendors/<int:vendor_id>/", vendor_details, name='details'),
    path("api/purchase_orders/", purchase_orders, name='orders'),
    path("api/purchase_orders/<int:po_id>/", update_orders, name='orders-details'),
    path("api/vendors/<int:vendor_id>/performance/", vendor_performance, name='performance'),
    path('api/vendors/performance/', vendor_performance, name='vendors_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge_purchase_order'),
]
