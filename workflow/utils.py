import pandas as pd
import pusher
import os

from workflow.serializers import ProductSerializer


def read_products_from_csv(test_file):
    """ Converts csv file into dataframe and then to a list of dictionaries """
    df = pd.read_csv(test_file)
    return df.to_dict('records')


# Configs for pusher websocket
pusher_client = pusher.Pusher(
    app_id=os.getenv("APP_ID"),
    key=os.getenv("KEY"),
    secret=os.getenv("SECRET"),
    cluster=os.getenv("CLUSTER")
)


def socket(data):
    """ Func to send websocket using pusher configs """
    pusher_client.trigger(
        os.getenv("CHANNEL_NAME"),
        os.getenv("CHANNEL_PASSWORD"),
        {'message': data}
    )


def save_into_db_with_serializer(product):
    """ Serializer to save products to database """
    serializer = ProductSerializer(data=product)
    if serializer.is_valid():
        serializer.save()
