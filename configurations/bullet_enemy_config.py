from dataclasses import dataclass


@dataclass
class BulletEnemyConfig:
    image: str
    velocity: int
    firing_interval: float