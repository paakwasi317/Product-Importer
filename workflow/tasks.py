from rest_framework.response import Response
from workflow.serializers import ProductSerializer
from celery import shared_task
from django.core.files.storage import default_storage
import os
from workflow.webhook import webhook
from workflow.utils import read_products_from_csv


@shared_task
def save_bulk_products_into_db(file_name):
    file = default_storage.open(file_name)
    products = read_products_from_csv(file)
    serializer = ProductSerializer(data=products, many=True)

    if serializer.is_valid():
        serializer.save()

    default_storage.delete(file_name)

    data = {
        "message": "All products uploaded successfully",
        "data": [],
        "successful": True,
        "error": ""
    }
    webhook("bulk_upload_done", data)

