from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
from io import BytesIO
import requests
import pandas as pd

# cache the data_extract step if same input is provided
# the cache will expire in 5 hours
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=5))
def data_extract(uri: str = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet'):
    response = requests.get(uri)

    if response.status_code != 200:
        raise Exception(response.text)
    else:
        df = pd.read_parquet(BytesIO(response.content))

    return df 

@flow(log_prints=True)
def etl_pipeline():
    df = data_extract()

if __name__ == '__main__':
    etl_pipeline()


