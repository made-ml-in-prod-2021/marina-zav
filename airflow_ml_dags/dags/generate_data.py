import os

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow_settings import VOLUMES, DEFAULT_ARGS, DATA_DIR

with DAG(
    "generate_data",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    start_date=days_ago(10),
) as dag:
    generate_data = DockerOperator(
        task_id="get_data",
        image="airflow-generate",
        command=os.path.join("/", DATA_DIR, "{{ ds }}"),
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    generate_data
