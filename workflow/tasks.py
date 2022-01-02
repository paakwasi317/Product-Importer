from celery import shared_task
from workflow.webhook import webhook
from workflow.utils import socket, save_into_db_with_serializer


@shared_task
def send_socket(percentage: str):
    """ Sends websocket of percentage of uploaded products """

    socket(percentage)


@shared_task
def save_bulk_products_into_db(products: list):
    """ Saves products into database and calculates percentage of uploaded products """

    counter = 0
    send_socket.delay('1')
    for product in products:
        save_into_db_with_serializer(product)
        counter = counter + 1
        percentage = (counter / len(products) * 100)
        if percentage % 2 == 0:
            print(percentage)
            send_socket.delay(f'{int(percentage)}')  # sends websocket with percentage to help stream uploaded products

    data = {
        "message": "All products uploaded successfully",
        "data": [],
        "successful": True,
        "error": ""
    }
    webhook("bulk_upload_done", data)

