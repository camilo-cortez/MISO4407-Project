import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.screen_properties import ScreenProperties


def system_collision_enemy_screen(world: esper.World, screen_props: ScreenProperties):
    # Rectángulo del área de juego con margen
    scr_rect = screen_props.scr_rect_margin

    components = world.get_components(
        CTransform, CSurface, CVelocity, CTagEnemy)

    # Paso 1: Detectar si algún enemigo toca el borde
    change_direction = False
    for entity, (c_t, c_s, c_v, _) in components:
        enemy_rect = pygame.Rect(c_t.pos.x, c_t.pos.y,
                                 c_s.area.width, c_s.area.height)

        if enemy_rect.left <= scr_rect.left or enemy_rect.right >= scr_rect.right:
            change_direction = True
            break

    # Paso 2: Cambiar la dirección si es necesario
    if change_direction:
        for entity, (c_t, c_s, c_v, _) in components:
            c_v.vel.x *= -1
