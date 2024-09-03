# Django specific imports
from django.urls import path, include

# Third party imports
from rest_framework.routers import DefaultRouter

# Local application imports
from .views import (
    LeadViewSet,
    LeadsBetweenDates,
    TopTenProducts,
    BottomTenProducts,
    ProductsInquiredCount,
)

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')

urlpatterns = [
    path('', include(router.urls)),

    # Custom APIView URLs
    path('leads-between-dates/', LeadsBetweenDates.as_view(), name='leads-between-dates'),
    path('top-ten-products/', TopTenProducts.as_view(), name='top-ten-products'),
    path('bottom-ten-products/', BottomTenProducts.as_view(), name='bottom-ten-products'),
    path('products-inquired-count/', ProductsInquiredCount.as_view(), name='products-inquired-count'),
]