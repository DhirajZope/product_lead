# Third party imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Local application imports
from .serializers import LeadSerializer
from .services import LeadService


class LeadViewSet(viewsets.ModelViewSet):
    queryset = LeadService.list_lead()
    serializer_class = LeadSerializer
    permission_classes = [AllowAny]


class LeadsBetweenDates(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        leads = LeadService.get_leads_between_dates(start_date, end_date)
        return Response(leads, status=status.HTTP_200_OK)


class TopTenProducts(APIView):
    def get(self, request):
        products = LeadService.get_top_ten_products()
        return Response(products, status=status.HTTP_200_OK)


class BottomTenProducts(APIView):
    def get(self, request):
        products = LeadService.get_bottom_ten_products()
        return Response(products, status=status.HTTP_200_OK)


class ProductsInquiredCount(APIView):
    def get(self, request):
        leads = LeadService.product_enquired()
        return Response(leads, status=status.HTTP_200_OK)
