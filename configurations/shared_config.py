from dataclasses import dataclass
from typing import List


@dataclass
class Size:
    x: int
    y: int


@dataclass
class Color:
    r: int
    g: int
    b: int


@dataclass
class Position:
    x: int
    y: int
