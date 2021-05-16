import logging
import pickle
from typing import Dict, Union

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, f1_score, log_loss
from sklearn.pipeline import Pipeline

from ml_project.entities.train_params import TrainingParams

SklearnRegressionModel = Union[RandomForestClassifier, LogisticRegression]
logger = logging.getLogger("logger")


def train_model(
    features: pd.DataFrame, target: pd.Series, train_params: TrainingParams
) -> SklearnRegressionModel:
    if train_params.model_type == "RandomForestClassifier":
        model = RandomForestClassifier(
            n_estimators=100, random_state=train_params.random_state
        )
    elif train_params.model_type == "LogisticRegression":
        model = LogisticRegression(random_state=train_params.random_state)
    elif train_params.model_type == "CatBoostClassifier":
        model = CatBoostClassifier(
            verbose=train_params.verbose, random_state=train_params.random_state
        )
    else:
        raise NotImplementedError(f"Unknown model type: {train_params.model_type}")
    model.fit(features, target)
    return model


def predict_model(model: Pipeline, features: pd.DataFrame) -> np.ndarray:
    predicts = model.predict(features)
    return predicts


def evaluate_model(predicts: np.ndarray, target: pd.Series) -> Dict[str, float]:
    return {
        "roc_auc": roc_auc_score(target, predicts),
        "f1": f1_score(target, predicts),
        "log_loss": log_loss(target, predicts),
    }


def create_inference_pipeline(
    model: SklearnRegressionModel, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([("feature_part", transformer), ("model_part", model)])


def serialize_model(model: object, output: str) -> str:
    with open(output, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"trained model saved to {output}")
    return output


def deserialize_model(path: str):
    with open(path, "rb") as f:
        model = pickle.load(f)
    logger.info(f"model loaded from {path}")
    return model
