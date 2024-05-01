import pygame

from configurations.shared_config import Position


class ScreenProperties:
    def __init__(self, screen: pygame.Surface, margin: int):
        # Original properties
        self.margin = margin
        self.center = Position(x=screen.get_width() // 2,
                               y=screen.get_height() // 2)
        self.top_left = Position(x=0, y=0)
        self.top_right = Position(x=screen.get_width(), y=0)
        self.bottom_left = Position(x=0, y=screen.get_height())
        self.bottom_right = Position(
            x=screen.get_width(), y=screen.get_height())

        # Properties with margins

        self.top_left_margin = Position(x=margin, y=margin)
        self.top_right_margin = Position(
            x=screen.get_width() - margin, y=margin)
        self.bottom_left_margin = Position(
            x=margin, y=screen.get_height() - margin)
        self.bottom_right_margin = Position(
            x=screen.get_width() - margin, y=screen.get_height() - margin)
