from django.urls import path

from .views import ProductListCreateAPIView ,CategoryListCreateAPIView


urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
]