
import random

import pygame

import esper
from configurations.player_config import PlayerConfig
from configurations.shared_config import Position
from configurations.starfield_config import StarFieldConfig
from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_star_spawner import CStarSpawner, StarSpawnEvent
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


def create_star_spawner(world: esper.World, config: StarFieldConfig, screen_props: ScreenProperties):
    spawner_entity = world.create_entity()

    # Cada medio segundo verifica las estrellas
    spawner = CStarSpawner(update_frequency=0.5)
    for _ in range(config.number_of_stars):
        x = random.uniform(0, screen_props.width)
        y = random.uniform(0, screen_props.height)
        color = random.choice(config.star_colors)
        speed = random.uniform(config.vertical_speed.min,
                               config.vertical_speed.max)
        blink_rate = random.uniform(
            config.blink_rate.min, config.blink_rate.max)
        size = random.randint(1, 3)
        spawner.spawn_events.append(StarSpawnEvent(
            x, y, color, speed, blink_rate, size, active=True))

    world.add_component(spawner_entity, spawner)
