from dataclasses import dataclass, field
from typing import List

from configurations.shared_config import Color


@dataclass
class StarSpawnEvent:
    x: float
    y: float
    color: Color
    speed: float
    blink_rate: float
    size: int
    active: bool = True  # Si la estrella está activa y visible
    time_since_blink: float = 0.0  # Tiempo desde el último cambio de visibilidad


@dataclass
class CStarSpawner:
    spawn_events: List[StarSpawnEvent] = field(default_factory=list)
    # Cada cuánto tiempo se verifica para reiniciar posiciones
    update_frequency: float = 0
    last_update_time: float = 1
