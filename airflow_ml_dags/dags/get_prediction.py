import os

from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from airflow_settings import (
    VOLUMES,
    DEFAULT_ARGS,
    DATA_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    SENSOR_ARGS,
)

with DAG(
    "get_prediction",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    start_date=days_ago(10),
) as dag:
    default_dir = os.path.join(
        MODEL_DIR, f"{sorted(os.listdir(MODEL_DIR), reverse=True)[0]}"
    )
    ACTUAL_MODEL_DIR = Variable.get("ACTUAL_MODEL_DIR", default_dir)

    data_sensor = FileSensor(
        task_id="1_data_sensor",
        filepath=os.path.join(DATA_DIR, "{{ ds }}", "data.csv"),
        **SENSOR_ARGS,
    )

    scaler_sensor = FileSensor(
        task_id="2_scaler_sensor",
        filepath=os.path.join(ACTUAL_MODEL_DIR, "scaler.pkl"),
        **SENSOR_ARGS,
    )

    model_sensor = FileSensor(
        task_id="3_model_sensor",
        filepath=os.path.join(ACTUAL_MODEL_DIR, "model.pkl"),
        **SENSOR_ARGS,
    )

    predict = DockerOperator(
        task_id="4_get_prediction",
        image="airflow-predict",
        command=[
            os.path.join("/", DATA_DIR, "{{ ds }}"),
            os.path.join("/", ACTUAL_MODEL_DIR),
            os.path.join("/", OUTPUT_DIR, "{{ ds }}"),
        ],
        network_mode="bridge",
        do_xcom_push=False,
        volumes=VOLUMES,
    )

    [data_sensor, scaler_sensor, model_sensor] >> predict
