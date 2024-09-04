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
        """
        Retrieve a queryset containing all Lead instances.

        Returns:
            QuerySet[Lead]: A queryset of all leads in the database.
        """
        return Lead.objects.all()

    @classmethod
    def get_leads_between_dates(cls, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Retrieve leads created between the specified start and end dates.

        Args:
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            List[Dict[str, Any]]: A list of serialized lead data for leads created between the given dates.
        """
        start_date = cls._convert_date_str_to_datetime(start_date)
        end_date = cls._convert_date_str_to_datetime(end_date)
        print(start_date, end_date)
        leads = Lead.objects.filter(created_at__range=[start_date, end_date])
        serializer = LeadSerializer(leads, many=True)
        return serializer.data

    @classmethod
    def get_top_ten_products(cls) -> List[Dict[str, Any]]:
        """
       Retrieve the top 10 products with the highest number of associated leads.

       Returns:
           List[Dict[str, Any]]: A list of serialized product data for the top 10 products with the most leads.
       """
        products = Product.objects.annotate(
            lead_count=Count('lead')
        ).prefetch_related(
            Prefetch('leads', queryset=Lead.objects.only('id'))
        ).order_by('-lead_count')[:10]

        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @classmethod
    def get_bottom_ten_products(cls) -> List[Dict[str, Any]]:
        """
        Retrieve the bottom 10 products with the fewest number of associated leads.

        Returns:
            List[Dict[str, Any]]: A list of serialized product data for the bottom 10 products with the fewest leads.
        """
        products = (
            Product.objects.annotate(
                lead_count=Count('lead')
            ).prefetch_related(
                Prefetch('leads', queryset=Lead.objects.only('id'))
            ).order_by('lead_count')[:10]
        )

        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @classmethod
    def product_enquired(cls) -> List[Dict[str, Any]]:
        """
        Retrieve the count of products each lead has inquired about.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary contains the lead's name
            and the number of products they have inquired about.
        """
        leads = Lead.objects.annotate(
            products_count=Count('interested_products')
        ).values('name', 'products_count')

        return list(leads)

    @classmethod
    def _convert_date_str_to_datetime(cls, date_str: str):
        """
        Convert a string representing a date in 'YYYY-MM-DD' format into a datetime.date object.

        Args:
            date_str (str): The date string to convert.

        Returns:
            datetime.date: A date object corresponding to the given date string.
        """
        return datetime.strptime(date_str, '%Y-%m-%d').date()
