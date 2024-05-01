import pygame

import esper
from configurations.shared_config import Position
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(world: esper.World, size: pygame.Vector2, color: pygame.Color,
                  pos: Position, vel: Position) -> int:
    entity = world.create_entity()

    world.add_component(entity, CSurface(size, color))

    world.add_component(entity, CTransform(
        pygame.Vector2(pos.x, pos.y)))

    if vel is not None:
        world.add_component(entity, CVelocity(
            pygame.Vector2(vel.x, vel.y)))
    return entity


def create_sprite(world: esper.World, pos: Position, vel: Position,
                  surface: pygame.Surface) -> int:
    entity = world.create_entity()

    world.add_component(entity, CSurface.from_surface(surface))

    world.add_component(entity, CTransform(
        pygame.Vector2(pos.x, pos.y)))

    if vel is not None:
        world.add_component(entity, CVelocity(
            pygame.Vector2(vel.x, vel.y)))
    return entity
