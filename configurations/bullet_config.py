from dataclasses import dataclass


@dataclass
class BulletConfig:
    sound: str
    image: str
    velocity: int
