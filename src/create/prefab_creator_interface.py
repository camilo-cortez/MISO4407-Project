from enum import Enum
from typing import Dict

import pygame

from configurations.interface_config import InterfaceItemConfig
import esper
from configurations.shared_config import Color, Position
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.screen_properties import ScreenProperties
from src.engine.service_locator import ServiceLocator


class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, txt: str, size: int,
                color: Color, pos: Position, alignment: TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get(
        "assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(
        txt, font, pygame.Color(color.r, color.g, color.b)))
    txt_s = world.component_for_entity(text_entity, CSurface)

    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pygame.Vector2(pos.x, pos.y) + origin))
    return text_entity


def create_blink_text(world: esper.World, txt: str, size: int,
                      color: Color, pos: Position, alignment: TextAlignment) -> int:
    text_entity = create_text(world, txt, size, color, pos, alignment)

    world.add_component(text_entity, CBlink(0.5))
    return text_entity


def create_1up_text(ecs_world, interface: Dict[str, InterfaceItemConfig], screen_props: ScreenProperties):
    return create_text(ecs_world, "1-UP", 8,
                       interface["title_text"].color,
                       Position(screen_props.top_left.x + 5,
                                screen_props.top_left.y + 5),
                       TextAlignment.LEFT)

def create_score_text(ecs_world, interface: Dict[str, InterfaceItemConfig], screen_props: ScreenProperties):
    return create_text(ecs_world, "000000", 8,
                       interface["normal_text"].color,
                       Position(screen_props.top_left.x + 10,
                                screen_props.top_left.y + 15),
                       TextAlignment.LEFT)
