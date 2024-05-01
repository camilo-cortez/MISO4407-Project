from dataclasses import dataclass


@dataclass
class Size:
    w: int
    h: int


@dataclass
class Color:
    r: int
    g: int
    b: int


@dataclass
class WindowConfig:
    title: str
    size: Size
    bg_color: Color
    framerate: int
