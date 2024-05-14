import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_hitbox import CHitbox, get_rect_relative

def system_rendering_debug_hitbox(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CHitbox)
    for _, (c_t, c_hit) in components:
        # HITBOX RECT
        ent_rect = get_rect_relative(c_hit.collider, c_t.pos)
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), ent_rect, 1)
