from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from configurations.animation_config import AnimationInfo


@dataclass
class EnemyConfig:
    sound: str
    image: str
    animations: Optional[AnimationInfo]
    score_value: int


class EnemyTypes(Enum):
    ENEMY_01 = 'Enemy01'
    ENEMY_02 = 'Enemy02'
    ENEMY_03 = 'Enemy03'
    ENEMY_04 = 'Enemy04'
