# src/ecs/systems/s_timer.py

import esper
from src.ecs.components.c_timer import CTimer
from src.engine.scenes.scene import Scene


def system_timer_to_scene(world: esper.World, delta_time: float, game_engine: Scene, next_scene: str):
    for entity, timer in world.get_component(CTimer):
        timer.accumulated_time += delta_time
        if timer.accumulated_time >= timer.duration:
            game_engine.switch_scene(next_scene)
