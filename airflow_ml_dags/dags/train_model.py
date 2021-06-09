import os

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from airflow_settings import (
    VOLUMES,
    DEFAULT_ARGS,
    SENSOR_ARGS,
    DATA_DIR,
    PROCESSED_DIR,
    MODEL_DIR,
    SPLITTED_DIR,
)

with DAG(
    "train_model",
    default_args=DEFAULT_ARGS,
    schedule_interval="@weekly",
    start_date=days_ago(10),
) as dag:
    data_sensor = FileSensor(
        task_id="1_data_sensor",
        filepath=os.path.join(DATA_DIR, "{{ ds }}", "data.csv") ** SENSOR_ARGS,
    )

    target_sensor = FileSensor(
        task_id="2_target_sensor",
        filepath=os.path.join(DATA_DIR, "{{ ds }}", "target.csv"),
        **SENSOR_ARGS
    )

    preprocess = DockerOperator(
        task_id="3_data_processing",
        image="airflow-preprocess",
        command=[
            os.path.join("/", DATA_DIR, "{{ ds }}"),
            os.path.join("/", PROCESSED_DIR, "{{ ds }}"),
            os.path.join("/", MODEL_DIR, "{{ ds }}"),
        ],
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    split = DockerOperator(
        task_id="4_data_splitting",
        image="airflow-split",
        command=[
            os.path.join("/", PROCESSED_DIR, "{{ ds }}"),
            os.path.join("/", SPLITTED_DIR, "{{ ds }}"),
        ],
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    train = DockerOperator(
        task_id="5_model_training",
        image="airflow-train",
        command=[
            os.path.join("/", SPLITTED_DIR, "{{ ds }}"),
            os.path.join("/", MODEL_DIR, "{{ ds }}"),
        ],
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    validate = DockerOperator(
        task_id="6_model_validation",
        image="airflow-validate",
        command=[
            os.path.join("/", SPLITTED_DIR, "{{ ds }}"),
            os.path.join("/", MODEL_DIR, "{{ ds }}"),
        ],
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    [data_sensor, target_sensor] >> preprocess >> split >> train >> validate
