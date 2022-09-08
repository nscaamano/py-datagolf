from dataclasses import dataclass


@dataclass
class Player:
    player_name: tuple
    dg_id: int
    amateur: int
    country: str
    country_code: str

