import pygame

import esper
from configurations.shared_config import Position
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


def create_logo(world: esper.World, position: Position) -> int:
    surface = ServiceLocator.images_service.get(
        "assets/img/invaders_logo_title.png")
    entity = create_sprite(world, position, None, surface)
    c_surface = world.component_for_entity(entity, CSurface)
    entity_rect = c_surface.surf.get_rect(
        center=(position.x, position.y))

    c_transform = world.component_for_entity(entity, CTransform)
    c_transform.pos = pygame.Vector2(entity_rect.x, entity_rect.y)
    return entity
