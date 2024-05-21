import esper
from src.create.prefab_creator_game import create_enemies_grid
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_level_transtition_timer import CLevelTransitionTimer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_check_enemies_and_restart(world: esper.World, delta_time: float, level_config, enemy_config, screen_props):
    enemy_entities = world.get_component(CTagEnemy)
    if not enemy_entities:
        # No hay enemigos, comenzamos o actualizamos el temporizador
        timer_entities = world.get_component(CLevelTransitionTimer)
        if not timer_entities:
            timer_entity = world.create_entity()
            world.add_component(timer_entity, CLevelTransitionTimer())
        else:
            for _, timer in timer_entities:
                timer.elapsed_time += delta_time
                if timer.elapsed_time >= timer.duration:
                    # Reiniciar el nivel
                    level_entities = world.get_component(CLevel)
                    for _, level in level_entities:
                        level.level += 1
                    create_enemies_grid(world, level_config,
                                        enemy_config, screen_props)
                    world.delete_entity(timer_entities[0][0])
    else:
        # Si hay enemigos, eliminamos cualquier temporizador existente
        timer_entities = world.get_component(CLevelTransitionTimer)
        for timer_entity, _ in timer_entities:
            world.delete_entity(timer_entity)
