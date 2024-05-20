import pygame


class CVelocity:
    def __init__(self, vel: pygame.Vector2, move_in_paused: bool = False) -> None:
        self.vel = vel
        self.move_in_paused = move_in_paused
