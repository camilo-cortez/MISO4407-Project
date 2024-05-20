import pygame

from configurations.global_config import GlobalConfig
from configurations.shared_config import Color, Position
from src.create.prefab_creator_game import create_stars
from src.create.prefab_creator_interface import TextAlignment, create_blink_text, create_text
from src.create.prefab_creator_menu import create_logo
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collition_enemy_screen import system_collision_enemy_screen
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_position import system_star_position
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    def __init__(self, config: GlobalConfig, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._paused = False
        self.config = config

    def do_create(self):
        create_stars(self.ecs_world, self.config.starfield,
                     self._game_engine.screen_props)

        interface = self._game_engine.config.interface
        create_logo(self.ecs_world, self._game_engine.screen_props.center)
        create_blink_text(self.ecs_world, "PRESS Z TO START", interface["title_text"].size,
                          interface["title_text"].color,
                          Position(self._game_engine.screen_props.center.x,
                                   self._game_engine.screen_props.center.y+30),
                          TextAlignment.CENTER)

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time: float):
        system_star_position(self.ecs_world, self._game_engine.screen_props)
        system_blink(self.ecs_world, delta_time)

        if not self._paused:
            system_movement(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        self.switch_scene("READY_SCENE")
