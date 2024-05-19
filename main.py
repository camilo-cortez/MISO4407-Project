#!/usr/bin/python3
"""Función Main"""

import asyncio

from configurations.global_config import GlobalConfig
from src.engine.game_engine import GameEngine

if __name__ == "__main__":
    defaultPath = './assets/cfg/'
    config = GlobalConfig(path=defaultPath)
    engine = GameEngine(config)
    asyncio.run(engine.run("MENU_SCENE"))