from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class GameState:
    # Personaje
    name: str = ""
    race: str = ""
    char_class: str = ""
    weapon: str = ""
    stats: Dict[str, int] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)

    # Progreso
    current_scene: str = "taberna"
    history: List[Dict[str, str]] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)  # eventos especiales
    game_over: bool = False
    ending_type: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "race": self.race,
            "char_class": self.char_class,
            "weapon": self.weapon,
            "stats": self.stats,
            "inventory": self.inventory,
            "current_scene": self.current_scene,
            "history": self.history,
            "flags": self.flags,
            "game_over": self.game_over,
            "ending_type": self.ending_type,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GameState":
        gs = cls()
        for k, v in d.items():
            setattr(gs, k, v)
        return gs

    def add_history(self, player_input: str, dm_response: str):
        self.history.append({"player": player_input, "dm": dm_response})

    def set_flag(self, flag: str):
        self.flags[flag] = True

    def has_flag(self, flag: str) -> bool:
        return self.flags.get(flag, False)
