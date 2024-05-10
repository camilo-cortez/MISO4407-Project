import random

import esper
from configurations.shared_config import Position
from src.create.prefab_creator import create_square
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.screen_properties import ScreenProperties


def system_blink(world: esper.World, delta_time: float):
    for entity, (blink, surface) in world.get_components(CBlink, CSurface):
        
        blink.time_since_blink += delta_time
        if blink.time_since_blink >= blink.blink_rate:
            blink.visible = not blink.visible
            blink.time_since_blink = 0
        surface.visible = blink.visible
