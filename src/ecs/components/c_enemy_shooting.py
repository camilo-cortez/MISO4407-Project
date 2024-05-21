import pygame
from dataclasses import dataclass

from configurations.bullet_config import BulletConfig
from configurations.level_config import ShootEnemysConfig


@dataclass
class CEnemyShooting:
    elapsed_time: float
    next_shoot_time: float
    shoot_config: ShootEnemysConfig
    bullet_config: BulletConfig
