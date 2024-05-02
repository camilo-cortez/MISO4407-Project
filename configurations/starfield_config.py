from dataclasses import dataclass
from typing import List

from configurations.shared_config import Color


@dataclass
class Speed:
    min: float
    max: float


@dataclass
class StarFieldConfig:
    star_colors: List[Color]
    vertical_speed: Speed
    blink_rate: Speed
    number_of_stars: int
