import pytest
from django.urls import reverse
import json
from workflow.models import Products


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_new_product_obj():
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
def test_create_product(api_client):
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
def test_get_all_products(api_client):
    url = reverse('Product-List-View')
    client = api_client
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_all_products(api_client):
    url = reverse('Product-List-View')
    client = api_client
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_one_product(api_client, create_new_product_obj):
    url = reverse('Product-Detail-View', kwargs={'product_id': create_new_product_obj.uuid})
    client = api_client
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_one_product(api_client, create_new_product_obj):
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
def test_filter_product(api_client):
    url = reverse('Product-Filter-View')
    client = api_client
    response = client.get(url, {'search': "Chris"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_active_product(api_client):
    url = reverse('Product-Status-Filter-View')
    client = api_client
    response = client.get(url, {'active': True})
    assert response.status_code == 200


@pytest.mark.django_db
def test_webhook(api_client):
    data = {
        "message": "Hello World"
    }
    url = reverse('Webhook-View')
    client = api_client
    response = client.post(url, data)
    assert response.status_code == 200
