import asyncio
from typing import Optional

import pygame

import esper
from configurations.global_config import GlobalConfig
from configurations.shared_config import Position
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_rendering import system_rendering
from src.engine.scenes.scene import Scene
from src.engine.screen_properties import ScreenProperties
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.game.ready_scene import ReadyScene


class GameEngine:
    def __init__(self, config: GlobalConfig) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(config.window.title)

        self.screen = pygame.display.set_mode(
            (config.window.size.w, config.window.size.h), pygame.SCALED)

        self._clock = pygame.time.Clock()
        self.is_running = False
        self.delta_time = 0
        self.config = config

        self._scenes: dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(config, self)
        self._scenes["READY_SCENE"] = ReadyScene(config, self)
        self._scenes["PLAY_SCENE"] = PlayScene(config, self)
        self._current_scene: Optional[Scene] = None
        self._scene_name_to_switch: str = None
        self.screen_props = ScreenProperties(self.screen, 10)

        self.ecs_world = esper.World()

    async def run(self, start_scene_name: str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            asyncio.sleep(0)
        self._do_clean()

    def switch_scene(self, new_scene_name: str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self._clock.tick(self.config.window.framerate)
        self.delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        color = self.config.window.bg_color
        self.screen.fill((color.r, color.g, color.b))
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action: CInputCommand):
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()
