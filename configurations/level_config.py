from dataclasses import dataclass
from typing import List

from configurations.enemy_config import EnemyTypes
from configurations.shared_config import Color


@dataclass
class GridConfig:
    type: str
    row: int
    positions: List[int]


@dataclass
class LevelConfig:
    enemys_grid: List[GridConfig]
