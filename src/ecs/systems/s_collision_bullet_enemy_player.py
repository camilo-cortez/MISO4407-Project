from configurations.explosion_config import ExplosionConfig
import esper
from src.create.prefab_creator_game import create_explosion
from src.ecs.components.c_hitbox import CHitbox, get_rect_relative
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy


def system_collision_bullet_player(world: esper.World, explosion_cfg: ExplosionConfig):
    player_components = world.get_components(
        CHitbox, CTransform, CSurface, CTagPlayer)
    bullet_components = world.get_components(
        CSurface, CTransform, CTagBulletEnemy)

    for bullet_entity, (bullet_surface, bullet_transform, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(
            bullet_surface.area, bullet_transform.pos)
        for player_entity, (player_hitbox, player_transform, player_surface, _) in player_components:
            player_rect = get_rect_relative(
                player_hitbox.collider, player_transform.pos)
            if bullet_rect.colliderect(player_rect):
                world.delete_entity(bullet_entity)
                player_surface.visible = False
                player_state = world.component_for_entity(
                    player_entity, CPlayerState)
                if player_state.state != PlayerState.DEAD:
                    player_state.state = PlayerState.DEAD
                    create_explosion(
                        world, player_transform.pos, explosion_cfg)
