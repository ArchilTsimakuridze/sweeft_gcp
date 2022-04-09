from google.cloud import storage
import datetime

from airflow import models
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


def check_if_updated(ds, **kwargs):
    """
    Receives a filename from cloud function and compares its hash value with
    its previous version hash value and if they match, return task it for
    python branch operator to trigger the next task
    :param ds: str
    :param kwargs: dict
    :return: str
    """
    blob = kwargs['dag_run'].conf['name']

    client = storage.Client()
    bucket = client.get_bucket('original-bucket')

    blobs = bucket.list_blobs(prefix=blob, versions=True)
    version_hash_list = []

    for blob in blobs:
        version_hash_list.append(blob.md5_hash)

    if version_hash_list[-1] != version_hash_list[-2]:
        print(f'Transferring {blob.name} to updated file bucket')
        return 'transfer_to_bucket'
    else:
        return None


default_args = {
    'owner': 'GCP Airflow',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': YESTERDAY,
}

with models.DAG(
        'transfer_updated',
        catchup=False,
        default_args=default_args,
        schedule_interval=None) as dag:

    hello_python = BranchPythonOperator(
        task_id='check_if_updated',
        python_callable=check_if_updated)

    t2 = BashOperator(
        task_id='transfer_to_bucket',
        bash_command="gsutil mv gs://maridashvili-bucket/{{ dag_run.conf['name'] }} gs://updated-bucket",
        dag=dag)

    hello_python >> t2




