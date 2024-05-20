
import random
from typing import Dict, List

import pygame

import esper
from configurations.bullet_config import BulletConfig
from configurations.enemy_config import EnemyConfig
from configurations.explosion_config import ExplosionConfig
from configurations.level_config import LevelConfig
from configurations.player_config import PlayerConfig
from configurations.shared_config import Position
from configurations.starfield_config import StarFieldConfig
from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_hitbox import CHitbox
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_score import CScore
from src.ecs.components.c_star_spawner import CStarSpawner, StarSpawnEvent
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_star import CTagStar
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

    player_fire_action = world.create_entity()
    world.add_component(player_fire_action,
                        CInputCommand("PLAYER_FIRE",
                                      pygame.K_z))


def create_player(world: esper.World, player_cfg: PlayerConfig, screen_props: ScreenProperties):
    surf = ServiceLocator.images_service.get(player_cfg.image)

    vel = Position(0, 0)
    pos_x = screen_props.center.x - surf.get_width() // 2
    pos_y = screen_props.bottom_left_margin.y - surf.get_height()
    entity = create_sprite(world, Position(pos_x, pos_y), vel, surf)
    world.add_component(entity, CAnimation(player_cfg.animations))
    world.add_component(entity, CTagPlayer())
    world.add_component(entity,
                        CHitbox(pygame.FRect(0, 0,
                                             surf.get_height(), surf.get_height())))
    world.add_component(entity, CPlayerState())
    return entity


def create_stars(world: esper.World, config: StarFieldConfig, screen_props: ScreenProperties):
    for _ in range(config.number_of_stars):
        x = random.uniform(0, screen_props.width)
        y = random.uniform(0, screen_props.height)
        color = random.choice(config.star_colors)
        speed = random.uniform(config.vertical_speed.min,
                               config.vertical_speed.max)
        blink_rate = random.uniform(
            config.blink_rate.min, config.blink_rate.max)
        star_entity = create_square(world, Position(
            1, 1), color, Position(x, y), Position(0, speed))
        velocity = world.component_for_entity(star_entity, CVelocity)
        velocity.move_in_paused = True
        world.add_component(star_entity, CTransform(Position(x, y)))
        world.add_component(star_entity, CBlink(blink_rate))
        world.add_component(star_entity, CTagStar())


def create_bullet(world: esper.World, pos_player: pygame.Vector2, bullet_cfg: BulletConfig, player_size: pygame.Vector2):
    bullet_surface = ServiceLocator.images_service.get(bullet_cfg.image)
    bullet_size = bullet_surface.get_rect().size
    vel_direction = pygame.Vector2(0, -1)
    vel = vel_direction * bullet_cfg.velocity
    pos = pygame.Vector2(pos_player.x + player_size.x/2 - (bullet_size[0] / 2),
                         pos_player.y + player_size.y/2 - (bullet_size[1] * 2))
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_cfg.sound)


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_cfg: ExplosionConfig):
    explosion_surf = ServiceLocator.images_service.get(explosion_cfg.image)
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surf)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_cfg.animations))
    ServiceLocator.sounds_service.play(explosion_cfg.sound)


def create_enemy(world: esper.World, pos: pygame.Vector2, enemy_info: EnemyConfig):
    enemy_surface = ServiceLocator.images_service.get(enemy_info.image)
    velocity = pygame.Vector2(10, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    width = enemy_surface.get_width() / enemy_info.animations.number_frames
    height = enemy_surface.get_height()
    world.add_component(enemy_entity, CAnimation(enemy_info.animations))
    world.add_component(enemy_entity, CTagEnemy(enemy_info.score_value))
    world.add_component(enemy_entity,
                        CHitbox(pygame.Rect(0, 0, width, height)))
    return enemy_entity


def create_enemies_grid(world: esper.World, level_config: LevelConfig, enemy_types: Dict[str, EnemyConfig], screen_props: ScreenProperties):
    row_height = 15  # Altura en píxeles entre cada fila de enemigos.
    column_width = 18  # Ancho en píxeles entre cada columna de enemigos.
    start_y = 40  # Posición inicial y desde donde comienzan los enemigos.
    # Calcula el número máximo de columnas de enemigos
    max_columns = max(len(row_info.positions)
                      for row_info in level_config.enemys_grid)
    total_grid_width = max_columns * column_width

    # Calcula start_x para centrar la grilla
    start_x = (screen_props.width - total_grid_width) // 2

    # Iteramos a través de la configuración del nivel para crear la grilla de enemigos
    for row_info in level_config.enemys_grid:
        enemy_type = enemy_types[row_info.type]
        y = start_y + row_info.row * row_height
        for col in row_info.positions:
            x = start_x + col * column_width
            create_enemy(world, pygame.Vector2(x, y), enemy_type)


def create_score(world: esper.World):
    score_entity = world.create_entity()
    world.add_component(score_entity, CScore())
    return score_entity
