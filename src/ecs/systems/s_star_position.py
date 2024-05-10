import random

import esper
from configurations.shared_config import Position
from src.create.prefab_creator import create_square
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.screen_properties import ScreenProperties


def system_star_position(world: esper.World, screen: ScreenProperties):
    for entity, (transform, _) in world.get_components(CTransform, CTagStar):
        if transform.pos.y > screen.height:
            transform.pos.y = 0
