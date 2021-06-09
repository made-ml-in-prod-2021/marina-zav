import sys
import pytest
from airflow.models import DagBag

sys.path.append("dags")


@pytest.fixture()
def dag_bag():
    return DagBag(dag_folder="dags/", include_examples=False)


def test_dag_bag_import(dag_bag):
    assert dag_bag.dags is not None
    assert dag_bag.import_errors == {}


def test_dag_generate_data_load(dag_bag):
    assert "generate_data" in dag_bag.dags
    assert len(dag_bag.dags["generate_data"].tasks) == 1


def test_dag_train_model_load(dag_bag):
    assert "train_model" in dag_bag.dags
    assert len(dag_bag.dags["train_model"].tasks) == 6


def test_dag_get_prediction_load(dag_bag):
    assert "get_prediction" in dag_bag.dags
    assert len(dag_bag.dags["get_prediction"].tasks) == 4


def test_dag_generate_data_structure(dag_bag):
    structure = {
        "get_data": [],
    }
    dag = dag_bag.dags["generate_data"]
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids


def test_dag_train_model_structure(dag_bag):
    structure = {
        "1_data_sensor": ["3_data_processing"],
        "2_target_sensor": ["3_data_processing"],
        "3_data_processing": ["4_data_splitting"],
        "4_data_splitting": ["5_model_training"],
        "5_model_training": ["6_model_validation"],
        "6_model_validation": [],
    }
    dag = dag_bag.dags["train_model"]
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids


def test_dag_get_prediction_structure(dag_bag):
    structure = {
        "1_data_sensor": ["4_get_prediction"],
        "2_scaler_sensor": ["4_get_prediction"],
        "3_model_sensor": ["4_get_prediction"],
        "4_get_prediction": [],
    }
    dag = dag_bag.dags["get_prediction"]
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids
