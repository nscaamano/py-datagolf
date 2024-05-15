from pydantic import BaseModel, confloat, conint
from datetime import date 
from typing import List

class PlayerModel(BaseModel):
    dg_id: int 
    player_name: str
    country: str
    country_code: str 
    amateur: conint(ge=0, le=1) 
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))
    
    
class EventModel(BaseModel):
    event_id: int 
    event_name: str 
    course_key: str 
    course: str 
    latitude: confloat(ge=-90, le=90)
    location: str 
    longitude: confloat(ge=-180, le=180)
    start_date: date 
    

class PlayerFieldUpdateModel(BaseModel):
    am: conint(ge=0, le=1) 
    country: str 
    course: str 
    dg_id: int # fk 
    dk_id: str 
    dk_salary: int 
    early_late: conint(ge=0, le=1)  # early is 1 
    fd_id: str 
    fd_salary: int 
    flag: str 
    pga_number: int 
    player_name: str 
    r1_teetime: str | None  
    r2_teetime: str | None 
    r3_teetime: str | None 
    r4_teetime: str | None 
    start_hole: int 
    unofficial: int 
    yh_id: str 
    yh_salary: int 
    
    def __hash__(self):
        return hash((self.dg_id))    
    

class PlayerFieldUpdatesModel(BaseModel):
    current_round: int 
    event_name: str 
    field: List[PlayerFieldUpdateModel]
    
    
class PlayerRankModel(BaseModel):
    am: conint(ge=0, le=1)
    country: str 
    datagolf_rank: int 
    dg_id: int # fk 
    dg_skill_estimate: float 
    owgr_rank: int 
    player_name: str 
    primary_tour: str 
    
class PreTournamentPredModel(BaseModel):
    am: conint(ge=0, le=1)
    country: str 
    dg_id: int # fk 
    make_cut: float 
    player_name: str 
    sample_size: int 
    top_10: float 
    top_20: float
    top_5: float
    win: float 
    
    