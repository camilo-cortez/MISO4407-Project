import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_screen_player(world: esper.World, screen_rect: pygame.Rect, margin: int):
    adjusted_screen_rect = pygame.Rect(
        screen_rect.x + margin,
        screen_rect.y + margin,
        screen_rect.width - 2 * margin,
        screen_rect.height - 2 * margin
    )
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    for _, (c_t, c_s, _) in components:
        paddle_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not adjusted_screen_rect.contains(paddle_rect):
            paddle_rect.clamp_ip(adjusted_screen_rect)
            c_t.pos.x = paddle_rect.x
            c_t.pos.y = paddle_rect.y
