import pandas as pd


def read_products_from_csv(test_file):
    df = pd.read_csv(test_file)
    return df.to_dict('records')
