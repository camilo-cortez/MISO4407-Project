
import random

import pygame

from configurations.bullet_config import BulletConfig
from configurations.enemy_config import EnemyConfig
from configurations.explosion_config import ExplosionConfig
import esper
from configurations.player_config import PlayerConfig
from configurations.shared_config import Position
from configurations.starfield_config import StarFieldConfig
from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_star_spawner import CStarSpawner, StarSpawnEvent
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
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
    
    player_fire_action = world.create_entity()
    world.add_component(player_fire_action,
                        CInputCommand("PLAYER_FIRE",
                                      pygame.K_SPACE))


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

def create_bullet(world:esper.World, pos_player:pygame.Vector2, bullet_cfg:BulletConfig, player_size:pygame.Vector2):
    bullet_surface = ServiceLocator.images_service.get(bullet_cfg.image)
    bullet_size = bullet_surface.get_rect().size
    vel_direction = pygame.Vector2(0,-1)
    vel = vel_direction * bullet_cfg.velocity
    pos = pygame.Vector2(pos_player.x + player_size.x/2 - (bullet_size[0] / 2 ),
                        pos_player.y + player_size.y/2 - (bullet_size[1] / 2 ))
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_cfg.sound)

def create_explosion(world:esper.World, pos:pygame.Vector2, explosion_cfg:ExplosionConfig):
    explosion_surf = ServiceLocator.images_service.get(explosion_cfg.image)
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surf)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_cfg.animations))
    ServiceLocator.sounds_service.play(explosion_cfg.sound)

def create_enemy(world:esper.World, pos:pygame.Vector2, enemy_info:EnemyConfig):
    enemy_surface = ServiceLocator.images_service.get(enemy_info.image)
    velocity = pygame.Vector2(0,0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())