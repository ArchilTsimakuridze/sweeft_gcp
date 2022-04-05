from google.cloud import storage
import datetime

from airflow import models
from airflow.operators import python_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


def some_func():
    client = storage.Client()
    bucket = client.get_bucket('maridashvili-bucket')

    blobs = bucket.list_blobs(versions=True)

    for blob in blobs:
        print(blob.md5_hash)


default_args = {
    'owner': 'Composer Example',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}

with models.DAG(
        'composer_quickstart',
        catchup=False,
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1)) as dag:

    hello_python = python_operator.PythonOperator(
        task_id='hello',
        python_callable=some_func)



