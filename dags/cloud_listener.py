from google.cloud import storage
import datetime

from airflow import models
from airflow.operators import python_operator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectUpdateSensor

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'Composer Example',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retry': False,
    'start_date': YESTERDAY,
}

with models.DAG(
        'composer_quickstart',
        catchup=False,
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1)) as dag:

    GCSObjectUpdateSensor(
        bucket='maridashvili-bucket',
        object='rame.csv',
        task_id='yleoba')

