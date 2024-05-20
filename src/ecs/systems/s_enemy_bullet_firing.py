import esper
import pygame
from src.ecs.components.c_enemy_firing import CEnemyFiring
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator_game import create_enemy_bullet
from configurations.bullet_enemy_config import BulletEnemyConfig

def system_enemy_bullet_firing(world: esper.World, delta_time: float, bullet_cfg: BulletEnemyConfig):
    components = world.get_components(CEnemyFiring, CTransform, CTagEnemy)
    
    for _, (c_firing, c_transform, _) in components:
        c_firing.time_since_last_shot += delta_time
        
        if c_firing.time_since_last_shot >= c_firing.firing_interval:
            create_enemy_bullet(world, c_transform.pos, bullet_cfg, c_transform.size)
            c_firing.time_since_last_shot = 0.0
