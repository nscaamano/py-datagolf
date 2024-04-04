from pydantic import BaseModel

class Player(BaseModel):
    dg_id: int 
    player_name: str
    country: str
    country_code: str 
    amateur: int 
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))