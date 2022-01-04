import pytest
from django.urls import reverse
from rest_framework.test import APIClient
import io
import csv
import json
from workflow.models import Products


@pytest.fixture
def api_client():  # An api client to make request
    return APIClient()


@pytest.fixture
def create_new_product_obj():  # A fixture for creating new products
    data = {
        "name": "John Edwards",
        "description": "Hello world",
        "sku": "movement-near",
        "active": True
    }
    product = Products(**data)
    product.save()
    return product


@pytest.mark.django_db
def test_create_product(api_client):  # Test for creating a product
    data = {
        "name": "Simeon Peter",
        "description": "It's a beautiful world",
        "sku": "move-here",
        "active": False
    }
    url = reverse('Product-List-View')
    client = api_client
    response = client.post(url, data, format='json')
    returned_data = json.loads(response.content)['data']
    assert response.status_code == 201
    assert returned_data['name'] == data['name']
    assert returned_data['description'] == data['description']
    assert returned_data['sku'] == data['sku']
    assert returned_data['active'] == data['active']


@pytest.mark.django_db
def test_get_all_products(api_client):  # Test for getting all products
    url = reverse('Product-List-View')
    client = api_client
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_all_products(api_client):  # Test for deleting all products
    url = reverse('Product-List-View')
    client = api_client
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_one_product(api_client, create_new_product_obj):  # Test for retrieving one product
    url = reverse('Product-Detail-View', kwargs={'product_id': create_new_product_obj.uuid})
    client = api_client
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_one_product(api_client, create_new_product_obj):  # Test for updating a product
    data = {
        "name": "Christopher Columbus",
        "active": True
    }
    url = reverse('Product-Detail-View', kwargs={'product_id': create_new_product_obj.uuid})
    client = api_client
    response = client.patch(url, data, format='json')
    returned_data = json.loads(response.content)['data']
    assert response.status_code == 201
    assert returned_data['name'] == "Christopher Columbus"
    assert returned_data['active'] == True


@pytest.mark.django_db
def test_filter_product(api_client):  # Test search by `name`, `description`, `sku`
    url = reverse('Product-Filter-View')
    client = api_client
    response = client.get(url, {'search': "Chris"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_active_product(api_client):  # Test for filtering by active and inactive products
    url = reverse('Product-Status-Filter-View')
    client = api_client
    response = client.get(url, {'active': True})
    assert response.status_code == 200


@pytest.mark.django_db
def test_webhook(api_client):  # Test for webhook
    data = {
        "message": "Hello World"
    }
    url = reverse('Webhook-View')
    client = api_client
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_bulk_upload(api_client):  # Test for bulk uploading of products
    """Creating CSV file to be uploaded"""
    csv_headers = ['name', 'description', 'sku', 'active']
    data = ['Raman', 'It works fine', 'hello-there', 'True']
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(csv_headers)
    writer.writerow(data)
    content = output.getvalue()
    encoded_content = content.encode('utf-8')
    bio = io.BytesIO(encoded_content)
    bio.seek(0)

    data = {
        "file": bio
    }
    url = reverse('Product-BulkUpload-View')
    client = api_client
    response = client.post(url, data)
    assert response.status_code == 200
