from dataclasses import dataclass


@dataclass
class CLevelTransitionTimer:
    elapsed_time: float = 0
    duration: float = 2.0
