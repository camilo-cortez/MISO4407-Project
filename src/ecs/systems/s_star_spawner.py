import random

import esper
from configurations.shared_config import Position
from src.create.prefab_creator import create_square
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_transform import CTransform
from src.engine.screen_properties import ScreenProperties


def system_star_spawner(world: esper.World, delta_time: float, screen: ScreenProperties):
    for ent, (spawner) in world.get_component(CStarSpawner):
        for event in spawner.spawn_events:
            # Actualizar el tiempo desde el último parpadeo
            event.time_since_blink += delta_time

            # Revisar si es tiempo de cambiar la visibilidad de la estrella
            relocate = event.time_since_blink >= event.blink_rate
            entity_exist = hasattr(
                event, 'entity') and world.entity_exists(event.entity)
            if relocate:
                event.active = not event.active
                event.time_since_blink = 0

                # Si la estrella debe desactivarse, se reposiciona y reactiva
                if not event.active:
                    event.y = random.uniform(0, screen.height)
                    event.x = random.uniform(0, screen.width)
                    event.active = True  # Reactivar la estrella para el siguiente ciclo

            # Revisar si la entidad de la estrella ya existe
            if entity_exist and relocate:
                transform = world.component_for_entity(
                    event.entity, CTransform)
                transform.pos.y = event.x
                transform.pos.x = event.y

            if not entity_exist:
                # Si no existe, crear la entidad y almacenarla en el evento
                star_entity = create_square(world, Position(1, 1), event.color, Position(
                    event.x, event.y), Position(0, event.speed))
                world.add_component(star_entity, CTransform(
                    Position(event.x, event.y)))
                event.entity = star_entity  # Guardar la referencia de la entidad en el evento

            # Asegurarse de que la visibilidad de la estrella es gestionada correctamente
            if event.active:
                if world.has_component(event.entity, CTransform):
                    transform = world.component_for_entity(
                        event.entity, CTransform)
                    transform.visible = True
            else:
                if world.has_component(event.entity, CTransform):
                    transform = world.component_for_entity(
                        event.entity, CTransform)
                    transform.visible = False
