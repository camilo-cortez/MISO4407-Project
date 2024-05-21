import json

import pygame

from configurations.shared_config import Position
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_hitbox import CHitbox
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.systems.s_collition_enemy_screen import system_collision_enemy_screen
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_refresh_score import system_refresh_score
import src.engine.game_engine
from configurations.global_config import GlobalConfig
from src.create.prefab_creator_game import (create_bullet, create_enemies_grid,
                                            create_enemy, create_game_input,
                                            create_player, create_score, create_stars)
from src.create.prefab_creator_interface import (TextAlignment, create_1up_text,
                                                 create_blink_text, create_pause_text, create_score_text,
                                                 create_text)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collision_bullet_enemy import \
    system_collision_bullet_enemy
from src.ecs.systems.s_delete_explosions import system_delete_explosions
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_star_position import system_star_position
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):
    def __init__(self, config: GlobalConfig, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._paused = False
        self.config = config
        self.game_paused_sound = "assets/snd/game_paused.ogg"

    def do_create(self):
        interface = self._game_engine.config.interface
        paused_text_ent = create_pause_text(
            self.ecs_world, interface, self._game_engine.screen_props)

        self.p_txt_s = self.ecs_world.component_for_entity(
            paused_text_ent, CSurface)
        self.p_txt_b = self.ecs_world.component_for_entity(
            paused_text_ent, CBlink)
        self._paused = False
        self.p_txt_s.visible = self._paused

        self.player_entity = create_player(self.ecs_world,
                                           self.config.player,
                                           self._game_engine.screen_props)

        self._p_v = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)

        self._p_t = self.ecs_world.component_for_entity(
            self.player_entity, CTransform)

        self._p_s = self.ecs_world.component_for_entity(
            self.player_entity, CSurface)

        # score
        create_1up_text(
            self.ecs_world, interface, self._game_engine.screen_props)
        self.score_text_ent = create_score_text(
            self.ecs_world, interface, self._game_engine.screen_props)
        self.p_txt_score = self.ecs_world.component_for_entity(
            paused_text_ent, CSurface)
        self.score_entity = create_score(self.ecs_world)
        create_game_input(self.ecs_world)
        create_stars(self.ecs_world, self.config.starfield,
                     self._game_engine.screen_props)

        create_enemies_grid(
            self.ecs_world, self.config.level_01, self.config.enemy, self._game_engine.screen_props)

    def do_update(self, delta_time: float):
        system_screen_player(self.ecs_world, self.screen_rect,
                             self._game_engine.screen_props.margin)

        system_star_position(self.ecs_world, self._game_engine.screen_props)
        system_collision_enemy_screen(
            self.ecs_world, self._game_engine.screen_props)

        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time, self._paused)
        if not self._paused:

            system_screen_bullet(self.ecs_world, self.screen_rect)
            system_collision_bullet_enemy(
                self.ecs_world, self.config.enemy_explosion, self.score_entity)
            system_player_state(self.ecs_world)
            system_refresh_score(self.ecs_world, self.score_text_ent)
            system_animation(self.ecs_world, delta_time)
            system_delete_explosions(self.ecs_world)

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
        elif action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                player_size = pygame.Vector2(
                    self._p_s.area.size[0], self._p_s.area.size[1])
                max_bullets = 1
                current_bullets = len(self.ecs_world.get_component(CTagBullet))
                if (current_bullets < max_bullets):
                    create_bullet(self.ecs_world, self._p_t.pos,
                                  self.config.bullet, player_size)
        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
            self.p_txt_b.active = self._paused
            if self._paused:
                ServiceLocator.sounds_service.play(self.game_paused_sound)
        if action.name == "GAME_OVER" and action.phase == CommandPhase.START: #TODO: use player death event
            self.switch_scene("GAME_OVER_SCENE")
