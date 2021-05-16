from dataclasses import dataclass, field


@dataclass()
class PreprocessParams:
    ohe_drop: str = field(default="if_binary")
