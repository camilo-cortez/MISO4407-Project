import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_screen_bullet(world:esper.World, screen_rect:pygame.Rect):
    components = world.get_components(CSurface, CTransform, CTagBullet)

    c_s:CSurface
    c_t:CTransform
    c_b:CTagBullet
    for bullet_entity, (c_s, c_t, _) in components:
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(bullet_rect):
            world.delete_entity(bullet_entity)