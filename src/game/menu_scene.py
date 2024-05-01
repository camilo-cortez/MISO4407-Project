import pygame

from configurations.shared_config import Color, Position
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.create.prefab_creator_menu import create_logo
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene


class MenuScene(Scene):

    def do_create(self):
        interface = self._game_engine.config.interface
        create_logo(self.ecs_world, self._game_engine.screen_props.center)
        create_text(self.ecs_world, "PRESS Z TO START", interface["title_text"].size,
                    interface["title_text"].color,
                    Position(self._game_engine.screen_props.center.x,
                             self._game_engine.screen_props.center.y+30),
                    TextAlignment.CENTER)

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("PLAY_SCENE")
