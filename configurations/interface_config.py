from dataclasses import dataclass
from configurations.shared_config import Color

@dataclass
class InterfaceItemConfig:
    size: int
    color: Color
