# Standard library imports
import logging
from typing import Dict, Any, Optional

# Django specific imports
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

# Local application imports
from .models import Product
from .serializers import ProductSerializer

# Global variable space
logger = logging.getLogger(__name__)


class ProductService:

    @classmethod
    def get_products(cls) -> QuerySet[Product]:
        """
        Fetch all products from the database

        Returns:
            - QuerySet : Queryset containing all products from the database.
        """
        return Product.objects.all()

    @classmethod
    def _get_unserialized_product(cls, product_id: int) -> Product:
        """
        Fetch a single product by its id.

        Args:
            product_id (int): ID if the product to fetch

        Returns:
            Product: The product instance of the specified product_id.

        Raises:
            ObjectDoesNotExists: If no product with specified id exists in the database.
        """
        return Product.objects.get(id=product_id)

    @classmethod
    def get_product(cls, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by its ID and serialize it.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns: Optional[Dict[str, Any]]: The serialized product data as a dictionary, or `None` if the product does
        not exist.

        """
        try:
            product = cls._get_unserialized_product(product_id)
            serializer = ProductSerializer(product)
            return serializer.data

        except ObjectDoesNotExist:
            logger.error(
                f"[ProductModule] - Product retrieval failed: Product with ID '{product_id}' does not exist."
            )
            return None

    @classmethod
    def create_product(cls, product_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new product using the provided information.

        Args:
            product_info (Dict[str, Any]): The product data to create.

        Returns: Optional[Dict[str, Any]]: `None` if the product is created successfully, or a dictionary of errors
        if validation fails.
        """
        serializer = ProductSerializer(data=product_info)

        if serializer.is_valid():
            serializer.save()
            return None
        return serializer.errors

    @classmethod
    def update_product(cls, product_id: int, product_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing product with the specified ID using the provided information.

        Args:
            product_id (int): The ID of the product to update.
            product_info (Dict[str, Any]): The updated product data.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing a success message if the update is successful,
            or a dictionary of errors if validation fails, or an error message if the product does not exist.
        """

        try:
            if "pkid" in product_info:
                product_info.pop("pkid")

            product = cls._get_unserialized_product(product_id)
            serializer = ProductSerializer(instance=product, data=product_info, partial=True)

            if serializer.is_valid():
                serializer.save()
                return {"message": "Product updated successfully."}
            return {"errors": serializer.errors}

        except ObjectDoesNotExist:
            logger.error(
                f"[ProductModule] - Product updation failed: Product with ID '{product_id}' does not exist."
            )
            return {f"error": f"Product with ID '{product_id}' does not exist."}

    @classmethod
    def delete_product(cls, product_id: int) -> bool:
        """
        Delete the product with the specified ID.

        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            bool: `True` if the product was successfully deleted, `False` if the product does not exist.
        """
        try:
            product = cls._get_unserialized_product(product_id)
            product.delete()
            return True
        except ObjectDoesNotExist:
            logger.error(
                f"[ProductModule] - Product deletion failed: Product with ID '{product_id}' does not exist."
            )
            return False
