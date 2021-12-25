"""
URL configuration for workflow module
"""
from django.urls import path
from workflow.views import ProductsListView, ProductsDetailView, DeleteAllProductsView

urlpatterns = [
    # POST & GET (Products)
    path("product", ProductsListView.as_view(), name="Product-List-View"),
    # DELETE, GET, PATCH (Products)
    path("product/<product_uuid>", ProductsDetailView.as_view(), name="Product-Detail-View"),
    # DELETE ALL (Products)
    path("product/deleteall", DeleteAllProductsView.as_view(), name="Delete-All_Product-View"),
]
