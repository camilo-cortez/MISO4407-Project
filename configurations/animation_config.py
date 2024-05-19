from dataclasses import dataclass
from typing import List

@dataclass
class Animation:
    name: str
    start: int
    end: int
    framerate: int

@dataclass
class AnimationInfo:
    number_frames: int
    list: List[Animation]
