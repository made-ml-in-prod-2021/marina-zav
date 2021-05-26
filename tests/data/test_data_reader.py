import pandas as pd
import pytest

from ml_project.data import split_train_val_data
from ml_project.entities.split_params import SplittingParams
import numpy as np


@pytest.fixture()
def some_test_df():
    return pd.DataFrame(np.random.rand(10, 10))


@pytest.fixture()
def splitting_params():
    return SplittingParams(0.4, 42)


def test_split_train_val_data(some_test_df, splitting_params):
    train_df, val_df = split_train_val_data(some_test_df, splitting_params)
    assert len(train_df) == 6
