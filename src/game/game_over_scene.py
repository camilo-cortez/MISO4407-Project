import pygame

from configurations.global_config import GlobalConfig
from configurations.shared_config import Color, Position
from src.create.prefab_creator_game import create_stars
from src.create.prefab_creator_interface import (TextAlignment,
                                                 create_1up_text,
                                                 create_blink_text,
                                                 create_score_text,
                                                 create_text)
from src.create.prefab_creator_menu import create_logo
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_timer import CTimer
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collition_enemy_screen import \
    system_collision_enemy_screen
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_position import system_star_position
from src.ecs.systems.s_timer_to_scene import system_timer_to_scene
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class GameOverScene(Scene):
    def __init__(self, config: GlobalConfig, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._paused = False
        self.config = config
        self.game_over_sound = "assets/snd/game_over.ogg"

    def do_create(self):
        create_stars(self.ecs_world, self.config.starfield,
                     self._game_engine.screen_props)

        interface = self._game_engine.config.interface
       
        create_text(self.ecs_world, "GAME OVER", 8,
                    interface["normal_text"].color,
                    Position(self._game_engine.screen_props.center.x,
                             self._game_engine.screen_props.center.y),
                    TextAlignment.CENTER)
        ServiceLocator.sounds_service.play(self.game_over_sound)
        timer_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(timer_entity, CTimer(3.0))

    def do_update(self, delta_time: float):
        system_blink(self.ecs_world, delta_time)
        system_timer_to_scene(self.ecs_world, delta_time,
                              self._game_engine, "MENU_SCENE")

        system_star_position(self.ecs_world, self._game_engine.screen_props)

        if not self._paused:
            system_movement(self.ecs_world, delta_time)
