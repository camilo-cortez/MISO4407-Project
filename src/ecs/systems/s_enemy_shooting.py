import random

import pygame

import esper
from configurations.level_config import ShootEnemysConfig
from src.create.prefab_creator_game import (create_enemy_bullet,
                                            create_player_bullet)
from src.ecs.components.c_enemy_shooting import CEnemyShooting
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_shooting(world: esper.World, delta_time: float, player_state: CPlayerState):
    if player_state.state.value < PlayerState.DEAD.value:

        for _, (enemy_shooting,) in world.get_components(CEnemyShooting):
            enemy_shooting.elapsed_time += delta_time

            if enemy_shooting.elapsed_time >= enemy_shooting.next_shoot_time:
                enemy_shooting.elapsed_time = 0
                enemy_shooting.next_shoot_time = random.uniform(
                    enemy_shooting.shoot_config.shoot_frecuency.min, enemy_shooting.shoot_config.shoot_frecuency.max)

                enemy_entities = [entity for entity,
                                  _ in world.get_component(CTagEnemy)]
                bullets_count = random.randint(
                    enemy_shooting.shoot_config.bullets_count.min, enemy_shooting.shoot_config.bullets_count.max)
                shooting_enemies = random.sample(
                    enemy_entities, min(bullets_count, len(enemy_entities)))

                for enemy in shooting_enemies:
                    enemy_transform = world.component_for_entity(
                        enemy, CTransform)
                    create_enemy_bullet(world, enemy_transform.pos,
                                        enemy_shooting.bullet_config, pygame.Vector2(0, 0))
