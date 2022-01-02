from django.shortcuts import render
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.storage import default_storage

from workflow.serializers import ProductSerializer
from workflow.models import Products
from workflow.pagination import StandardResultsSetPagination
from workflow.webhook import webhook


class ProductsListView(ListCreateAPIView):
    """
        This view allows the following:
            - GET Method: get all products with pagination
            - POST Method: create a new product
            - DELETE Method: bulk delete products
    """
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        products = Products.objects.all().order_by('-created_at')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Product created successfully",
                "data": serializer.data,
                "successful": True,
                "error": ""
            }
            webhook("created", data)
            return Response(data=data, status=status.HTTP_201_CREATED)

        data = {
            "message": "Product failed to create",
            "data": "",
            "successful": False,
            "error": serializer.errors
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        product = Products.objects.all()
        product.delete()
        data = {
            "message": "Products deleted successfully",
            "data": "",
            "successful": True,
            "error": ""
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class ProductsDetailView(APIView):
    """
        This view allows to Retrieve, update or delete
        a Product instance.
    """

    def get_object(self, product_id):
        try:
            return Products.objects.get(uuid=product_id)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, product_id):
        product = self.get_object(product_id)
        serializer = ProductSerializer(product)
        data = {
            "message": "Product retrieved successfully",
            "data": serializer.data,
            "successful": True,
            "error": ""
        }
        return Response(data=data)

    def patch(self, request, product_id):
        product = self.get_object(product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Product updated successfully",
                "data": serializer.data,
                "successful": True,
                "error": ""
            }
            webhook("updated", data)
            return Response(data=data, status=status.HTTP_201_CREATED)

        data = {
            "message": "Product failed to update",
            "data": "",
            "successful": False,
            "error": serializer.errors
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        product.delete()
        data = {
            "message": "Product deleted successfully",
            "data": "",
            "successful": True,
            "error": ""
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class ProductsBulkUploadView(APIView):
    """"
        This view is responsible for bulk-uploading of
        products
    """

    def post(self, request):
        from workflow.utils import read_products_from_csv
        from workflow.tasks import save_bulk_products_into_db

        product_file = request.data['file']
        products = read_products_from_csv(product_file)
        save_bulk_products_into_db.delay(products)  # saves products into db with async to prevent timeout
        data = {
            "message": "Product uploading ...",
            "data": [],
            "successful": True,
            "error": ""
        }

        return Response(data=data)


class ProductFilterList(generics.ListAPIView):
    """
        This view is responsible for searching for products by
        `name`, `description`, `active` and `sku`. It's more of
        the general search filter
    """
    queryset = Products.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'active', 'sku']


class ProductActiveFilterList(generics.ListAPIView):
    """
        This view is responsible for searching for product
        by `active` field. It helps to filter products by active or
        inactive products
    """
    queryset = Products.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']


class WebhookView(APIView):
    """
        This view is responsible for the webhooks
    """

    def post(self, request):
        data = request.data
        data = {
            "message": "Callback sent successful",
            "data": data,
            "successful": True,
            "error": ""
        }

        return Response(data=data)
