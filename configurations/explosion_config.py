from dataclasses import dataclass
from configurations.animation_config import AnimationInfo


@dataclass
class ExplosionConfig:
    sound: str
    image: str
    animations: AnimationInfo