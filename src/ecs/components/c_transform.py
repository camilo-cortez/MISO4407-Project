import pygame

from configurations.shared_config import Position


class CTransform:
    def __init__(self, pos: Position) -> None:
        self.pos = pygame.Vector2(pos.x, pos.y)
