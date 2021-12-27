"""
URL configuration for workflow module
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from workflow.views import ProductsListView, ProductsDetailView, ProductsBulkUploadView, ProductFilterList, ProductActiveFilterList, WebhookView

urlpatterns = [
    # POST, GET, DELETE (PRODUCTS
    path("product", ProductsListView.as_view(), name="Product-List-View"),
    # DELETE, GET, PATCH A PRODUCT
    path("product/<product_id>", ProductsDetailView.as_view(), name="Product-Detail-View"),
    # BULK UPLOAD OF PRODUCTS
    path("product/bulk/upload", ProductsBulkUploadView.as_view(), name="Product-BulkUpload-View"),
    # FILTER PRODUCTS BY ALL FIELDS
    path("product/values/filter", ProductFilterList.as_view(), name="Product-Filter-View"),
    # FILTER PRODUCTS BY STATUS(ACTIVE || INACTIVE)
    path("product/status/filter", ProductActiveFilterList.as_view(), name="Product-Filter-View"),
    # WEBHOOK URL
    path("webhook", WebhookView.as_view(), name="Webhook-View"),
]
urlpatterns = format_suffix_patterns(urlpatterns)