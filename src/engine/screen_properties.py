import pygame

from configurations.shared_config import Position


class ScreenProperties:
    def __init__(self, screen: pygame.Surface, margin: int):
        # Original properties
        self.margin = margin
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.center = Position(x=self.width // 2,
                               y=self.height // 2)
        self.top_left = Position(x=0, y=0)
        self.top_right = Position(x=self.width, y=0)
        self.bottom_left = Position(x=0, y=self.height)
        self.bottom_right = Position(
            x=self.width, y=self.height)

        # Properties with margins

        self.top_left_margin = Position(x=margin, y=margin)
        self.top_right_margin = Position(
            x=self.width - margin, y=margin)
        self.bottom_left_margin = Position(
            x=margin, y=self.height - margin)
        self.bottom_right_margin = Position(
            x=self.width - margin, y=self.height - margin)

        self.scr_rect_margin = pygame.Rect(self.top_left_margin.x, self.top_left_margin.y,
                                           self.width - 2 * self.margin, self.height - 2 * self.margin)
