from enum import Enum


class CPlayerState:
    def __init__(self) -> None:
        self.state = PlayerState.READY


class PlayerState(Enum):
    IDLE = 0
    READY = 1
    DEAD = 2
