import pygame

from configurations.shared_config import Position


class CBlink:
    def __init__(self, blink_rate: float, active: bool = True):
        self.blink_rate = blink_rate
        self.time_since_blink = 0
        self.visible = True
        self.active = active
