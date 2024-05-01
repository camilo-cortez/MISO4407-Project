
import pygame

import esper
from configurations.player_config import PlayerConfig
from configurations.shared_config import Position
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.screen_properties import ScreenProperties
from src.engine.service_locator import ServiceLocator


def create_game_input(world: esper.World):
    left_action = world.create_entity()
    world.add_component(left_action,
                        CInputCommand("LEFT",
                                      pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action,
                        CInputCommand("RIGHT",
                                      pygame.K_RIGHT))

    pause_action = world.create_entity()
    world.add_component(pause_action,
                        CInputCommand("PAUSE",
                                      pygame.K_p))


def create_player(world: esper.World, player_cfg: PlayerConfig, screen_props: ScreenProperties):
    surf = ServiceLocator.images_service.get(player_cfg.image)

    vel = Position(0, 0)
    pos_x = screen_props.center.x - surf.get_width() // 2
    pos_y = screen_props.bottom_left_margin.y - surf.get_height()
    entity = create_sprite(world, Position(pos_x, pos_y), vel, surf)
    world.add_component(entity, CTagPlayer())
    return entity
