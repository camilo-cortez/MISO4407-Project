from dataclasses import dataclass
from typing import Optional
from configurations.animation_config import AnimationInfo

@dataclass
class PlayerConfig:
    image: str
    input_velocity: int
    animations: Optional[AnimationInfo]
