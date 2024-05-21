from dataclasses import dataclass
from typing import List

from configurations.bullet_config import BulletConfig


@dataclass
class GridConfig:
    type: str
    row: int
    positions: List[int]


@dataclass
class EnemysShooting:
    min: int
    max: int


@dataclass
class ShootFrecuency:
    min: int
    max: int


@dataclass
class ShootEnemysConfig:
    bullets_count: EnemysShooting
    shoot_frecuency: ShootFrecuency
    bullet: BulletConfig


@dataclass
class LevelConfig:
    enemys_grid: List[GridConfig]
    shoot_enemys_config: ShootEnemysConfig
