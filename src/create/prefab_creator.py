import pygame

import esper
from configurations.shared_config import Color, Position
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(world: esper.World, size: Position, color: Color,
                  pos: Position, vel: Position) -> int:
    entity = world.create_entity()

    world.add_component(entity, CSurface(
        pygame.Vector2(size.x, size.y), pygame.Color(color.r, color.g, color.b)))

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
