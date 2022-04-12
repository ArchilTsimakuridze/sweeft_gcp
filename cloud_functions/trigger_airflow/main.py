from cloud_functions.trigger_airflow import composer2_airflow_rest_api


def trigger_dag_gcf(data, context=None):
    """
    Trigger a DAG and pass event data.

    Args:
      data: A dictionary containing the data for the event. Its format depends
      on the event. In this case data contains metadata of an uploaded file
      context: The context object for the event."""

    web_server_url = (
        "https://e375e93fbd0a467b86b5ed0b131988d8-dot-europe-west1.composer.googleusercontent.com"
    )

    # A string representing the dag that is going to be triggered
    dag_id = 'transfer_updated'

    composer2_airflow_rest_api.trigger_dag(web_server_url, dag_id, data)

    print(data)
