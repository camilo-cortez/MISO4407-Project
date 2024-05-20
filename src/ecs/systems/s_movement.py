import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(world: esper.World, delta_time: float, is_paused: bool = False):
    components = world.get_components(CTransform, CVelocity)
    for _, (c_t, c_v) in components:
        if not is_paused or c_v.move_in_paused:
            c_t.pos.x += c_v.vel.x * delta_time
            c_t.pos.y += c_v.vel.y * delta_time
