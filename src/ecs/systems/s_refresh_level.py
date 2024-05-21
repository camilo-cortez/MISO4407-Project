import pygame
import esper
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator

def system_refresh_level(world:esper.World, level_text_entity:int):
    components = world.get_component(CLevel)
    s_ui = world.component_for_entity(level_text_entity, CSurface)
    text_size = 8
    c_s:CLevel
    color = pygame.Color(255,255,255)
    for _, c_s in components:
        s_ui.surf = CSurface.from_text(str(c_s.level), 
                            ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", text_size), 
                            color).surf