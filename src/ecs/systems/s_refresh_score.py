import pygame
import esper
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator

def system_refresh_score(world:esper.World, score_text_entity:int):
    components = world.get_component(CScore)
    s_ui = world.component_for_entity(score_text_entity, CSurface)
    text_size = 8
    c_s:CScore
    color = pygame.Color(255,255,255)
    for _, c_s in components:
        s_ui.surf = CSurface.from_text(str(c_s.score), 
                            ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", text_size), 
                            color).surf
        
