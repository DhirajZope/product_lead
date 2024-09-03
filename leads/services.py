# Standard library imports
from typing import List, Dict, Any
from datetime import datetime

# Django specific imports
from django.db.models import QuerySet, Count, Prefetch

# Local application imports
from .models import Lead
from products.models import Product
from .serializers import LeadSerializer
from products.serializers import ProductSerializer


class LeadService:

    @classmethod
    def list_lead(cls) -> QuerySet[Lead]:
        return Lead.objects.all()

    @classmethod
    def get_leads_between_dates(cls, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        start_date = cls._convert_date_str_to_datetime(start_date)
        end_date = cls._convert_date_str_to_datetime(end_date)
        leads = Lead.objects.filter(created_at__range=[start_date, end_date])
        serializer = LeadSerializer(leads, many=True)
        return serializer.data

    @classmethod
    def get_top_ten_products(cls) -> List[Dict[str, Any]]:
        products = Product.objects.annotate(
            lead_count=Count('leads')
        ).prefetch_related(
            Prefetch('leads', queryset=Lead.objects.only('id'))
        ).order_by('-lead_count')[:10]

        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @classmethod
    def get_bottom_ten_products(cls) -> List[Dict[str, Any]]:
        products = (
            Product.objects.annotate(
                lead_count=Count('leads')
            ).prefetch_related(
                Prefetch('leads', queryset=Lead.objects.only('id'))
            ).order_by('lead_count')[:10]
        )

        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @classmethod
    def product_enquired(cls) -> List[Dict[str, Any]]:
        leads = Lead.objects.annotate(
            products_count=Count('interested_products')
        ).values('name', 'products_count')

        return list(leads)

    @classmethod
    def _convert_date_str_to_datetime(cls, date_str: str):
        return datetime.strptime(date_str, '%Y-%m-%d')
