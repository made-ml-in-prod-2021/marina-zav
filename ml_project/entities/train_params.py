from dataclasses import dataclass, field


@dataclass()
class TrainingParams:
    model_type: str = field(default="CatBoostClassifier")
    random_state: int = field(default=255)
    verbose: bool = field(default=False)
