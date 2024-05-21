import random

import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.screen_properties import ScreenProperties

def system_enemy_selection(world: esper.World, screen: ScreenProperties):
    number_enemies = world.get_components(CTransform, CTagEnemy)
    for entity, (transform, _) in number_enemies:
        for i in range(5):
            random = random.choice(number_enemies)
