from dataclasses import dataclass

import yaml
from marshmallow_dataclass import class_schema

from .feature_params import FeatureParams
from .preprocess_params import PreprocessParams
from .split_params import SplittingParams
from .train_params import TrainingParams


@dataclass()
class TrainingPipelineParams:
    input_data_path: str
    output_model_path: str
    metric_path: str
    splitting_params: SplittingParams
    preprocess_params: PreprocessParams
    feature_params: FeatureParams
    train_params: TrainingParams


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def read_training_pipeline_params(path: str) -> TrainingPipelineParams:
    with open(path, "r") as input_stream:
        schema = TrainingPipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))
