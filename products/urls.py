from django.urls import path
from .views import ProductListView, ProductView


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('', ProductView.as_view(), name='product-create'),
    path('<int:product_id>/', ProductView.as_view(), name='product-detail'),
]
