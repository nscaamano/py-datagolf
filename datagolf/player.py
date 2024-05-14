from .models import Player
from .api import DgAPI

'''
class Player(BaseModel):
    dg_id: int 
    player_name: str
    country: str
    country_code: str 
    amateur: conint(ge=0, le=1) 
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))
'''

class PlayerCombined:
    """Combines all available api data for a particular player.
    """
    
    def __init__(self, player_name, dg_id):
        self.api = DgAPI()