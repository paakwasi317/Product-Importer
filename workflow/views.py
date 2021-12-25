from django.shortcuts import render
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from workflow.serializers import ProductSerializer
from workflow.models import Products


class ProductsListView(APIView):

    def get(self, request):
        snippets = Products.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Retrieve, update or delete a Product instance.
    """

    def get_object(self, product_uuid):
        try:
            return Products.objects.get(uuid=product_uuid)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request,product_uuid):
        product = self.get_object(product_uuid)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, product_uuid):
        product = self.get_object(product_uuid)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_uuid):
        product = self.get_object(product_uuid)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
