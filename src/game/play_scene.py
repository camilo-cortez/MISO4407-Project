import json

import pygame

import src.engine.game_engine
from configurations.global_config import GlobalConfig
from src.create.prefab_creator_game import (create_game_input, create_player,
                                            create_star_spawner)
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_star_spawner import system_star_spawner
from src.engine.scenes.scene import Scene


class PlayScene(Scene):
    def __init__(self, config: GlobalConfig, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._paused = False
        self.config = config

    def do_create(self):
        interface = self._game_engine.config.interface

        paused_text_ent = create_text(self.ecs_world, "PAUSED", 16,
                                      interface["title_text"].color,
                                      self._game_engine.screen_props.center,
                                      TextAlignment.CENTER)

        self.p_txt_s = self.ecs_world.component_for_entity(
            paused_text_ent, CSurface)

        self.p_txt_s.visible = self._paused
        self._paused = False

        self.player_entity = create_player(self.ecs_world,
                                           self.config.player,
                                           self._game_engine.screen_props)

        self._p_v = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)

        create_game_input(self.ecs_world)
        create_star_spawner(self.ecs_world, self.config.starfield,
                            self._game_engine.screen_props)

    def do_update(self, delta_time: float):
        system_screen_player(self.ecs_world, self.screen_rect,
                             self._game_engine.screen_props.margin)
        system_star_spawner(
            self.ecs_world, self._game_engine.delta_time, self._game_engine.screen_props)
        if not self._paused:
            system_movement(self.ecs_world, delta_time)

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if action.name == "LEFT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x -= self.config.player.input_velocity
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x += self.config.player.input_velocity
        elif action.name == "RIGHT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x += self.config.player.input_velocity
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x -= self.config.player.input_velocity

        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
