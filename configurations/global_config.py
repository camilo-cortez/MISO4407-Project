from dataclasses import dataclass, field
from typing import Dict

from dacite import from_dict

from configurations.bullet_config import BulletConfig
from configurations.interface_config import InterfaceItemConfig
from configurations.player_config import PlayerConfig
from configurations.starfield_config import StarFieldConfig
from configurations.window_config import WindowConfig
from utils.json import load_json


@dataclass
class GlobalConfig:
    window: WindowConfig = field(init=False)
    starfield: StarFieldConfig = field(init=False)
    interface: Dict[str, InterfaceItemConfig] = field(init=False)
    player: PlayerConfig = field(init=False)
    bullet: BulletConfig = field(init=False)
    path: str

    def __post_init__(self):
        self._load_window_config()
        self._load_starfield_config()
        self._load_interface_config()
        self._load_player_config()
        self._load_bullet_config()

    def _load_window_config(self):
        self.window = self._load_config(WindowConfig, 'window.json')

    def _load_starfield_config(self):
        self.starfield = self._load_config(StarFieldConfig, 'starfield.json')

    def _load_player_config(self):
        self.player = self._load_config(PlayerConfig, 'player.json')
    
    def _load_bullet_config(self):
        self.bullet = self._load_config(BulletConfig, 'bullet.json')

    def _load_interface_config(self):
        data = load_json(self.path + 'interface.json')
        self.interface = {interface_key: from_dict(data_class=InterfaceItemConfig,
                                                   data=interface_data)
                          for interface_key, interface_data in data.items()}

    def _load_config(self, config_class, file_name):
        config_data = load_json(self.path + file_name)
        return from_dict(data_class=config_class, data=config_data)
