import pygame

class CHitbox:
    def __init__(self, collider:pygame.Rect) -> None:
        self.collider:pygame.Rect = collider

def get_rect_relative(rect:pygame.Rect, pos:pygame.Vector2):
    rect_copy = rect.copy()
    # Relativo a la posición del sprite, 
    # por eso topleft se suma y no se iguala
    rect_copy.topleft += pos
    return rect_copy