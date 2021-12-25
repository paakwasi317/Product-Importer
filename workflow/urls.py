"""
URL configuration for workflow module
"""
from django.urls import path
from workflow.views import ProductsListView, ProductsDetailView

urlpatterns = [
    # POST, GET, DELETE (PRODUCTS
    path("product", ProductsListView.as_view(), name="Product-List-View"),
    # DELETE, GET, PATCH A PRODUCT
    path("product/<product_uuid>", ProductsDetailView.as_view(), name="Product-Detail-View"),
]
