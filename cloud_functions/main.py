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
        "https://f4eb1d8fd596406b9619cbe9f8c65907-dot-europe-central2.composer.googleusercontent.com"
    )
    # Replace with the ID of the DAG that you want to run.
    dag_id = 'bucket_listener'

    composer2_airflow_rest_api.trigger_dag(web_server_url, dag_id, data)

    print(data)
