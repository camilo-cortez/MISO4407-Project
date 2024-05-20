class CEnemyFiring:
    def __init__(self, firing_interval: float) -> None:
        self.firing_interval = firing_interval
        self.time_since_last_shot = 0.0
