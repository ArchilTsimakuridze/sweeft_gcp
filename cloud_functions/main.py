from typing import Any

import composer2_airflow_rest_api


def trigger_dag_gcf(data, context=None):
    """
    Trigger a DAG and pass event data.

    Args:
      data: A dictionary containing the data for the event. Its format depends
      on the event.
      context: The context object for the event."""

    web_server_url = (
        "https://e375e93fbd0a467b86b5ed0b131988d8-dot-europe-west1.composer.googleusercontent.com"
    )
    # Replace with the ID of the DAG that you want to run.
    dag_id = 'transfer_updated'

    composer2_airflow_rest_api.trigger_dag(web_server_url, dag_id, data)

    print(data)
