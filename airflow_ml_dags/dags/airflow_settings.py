from datetime import timedelta

VOLUMES = [
    "/Users/marina/Projects/made2020/ml_in_prod/HW3/marina-zav/airflow_ml_dags/data/:/data"
]

DEFAULT_ARGS = {
    "owner": "MarinaZav",
    "email_on_failure": True,  # Alert в случае падения дага
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": True,
}

SENSOR_ARGS = {"poke_interval": 10, "timeout": 60, "mode": "reschedule"}

DATA_DIR = "data/raw"
MODEL_DIR = "data/model"
OUTPUT_DIR = "data/output"
PROCESSED_DIR = "data/processed"
SPLITTED_DIR = "data/splitted"
