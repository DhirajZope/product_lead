# Django specific imports
from django.shortcuts import render

# Third party imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

# Local application imports
from .services import ProductService
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    queryset = ProductService.get_products()
    serializer_class = ProductSerializer


class ProductView(APIView):

    def get(self, _, product_id: int):
        product = ProductService.get_product(product_id)

        if product is None:
            return Response(
                {"error": "Product you are looking for is not exists."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(product, status=status.HTTP_200_OK)

    def post(self, request):
        product_info = request.data
        errors = ProductService.create_product(product_info)

        if errors is not None:
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(
            {"message": "Product created successfully."},
            status=status.HTTP_201_CREATED
        )

    def patch(self, request, product_id: int):
        data_to_update = request.data
        update_status = ProductService.update_product(product_id, data_to_update)

        if update_status is None:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if "error" in update_status:
            return Response(update_status, status=status.HTTP_404_NOT_FOUND)

        if "errors" in update_status:
            return Response(update_status, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(update_status, status=status.HTTP_200_OK)

    def delete(self, product_id: int):
        is_deleted = ProductService.delete_product(product_id)

        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)