from django.urls import path

from .views import StoreListCreateAPIView,StoreInventoryAPIView,StoreOrdersAPIView


urlpatterns = [
    path("", StoreListCreateAPIView.as_view(), name="store-list-create"),
    path("<int:store_id>/inventory/",StoreInventoryAPIView.as_view(),name="store-inventory"),
    path("<int:store_id>/orders/",StoreOrdersAPIView.as_view(),name="store-orders"),
]