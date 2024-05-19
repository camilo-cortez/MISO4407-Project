import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_player_state(world:esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)
    num_bullets = len(world.get_components(CTagBullet))
    for _, (c_v, c_a, c_pst) in components:
        if c_pst.state == PlayerState.IDLE:
            _do_idle_state(c_v, c_a, c_pst, num_bullets)
        elif c_pst.state == PlayerState.READY:
            _do_ready_state(c_v, c_a, c_pst, num_bullets)

def _do_idle_state(c_v:CVelocity, c_a:CAnimation, c_pst:CPlayerState, num_bullets:int):
    _set_animation(c_a, 1)
    if num_bullets == 0:
        c_pst.state = PlayerState.READY

def _do_ready_state(c_v:CVelocity, c_a:CAnimation, c_pst:CPlayerState, num_bullets:int):
    _set_animation(c_a, 0)
    if num_bullets > 0:
        c_pst.state = PlayerState.IDLE

def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.current_animation == num_anim:
        return
    c_a.current_animation = num_anim
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animations_list[c_a.current_animation].start