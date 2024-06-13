from pydantic import BaseModel, confloat, conint, Field
from datetime import date, datetime
from typing import List, Optional, Union, Set


class PlayerModel(BaseModel):
    dg_id: int 
    player_name: str
    country: str
    country_code: str 
    amateur: bool
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))
    
    
class EventModel(BaseModel):
    '''
        event_id is not unique 
        'TBD' used for some
        Seen duplicates across tours 
        for example 
    '''
    event_id: Union[str, int] # no good includes 'TBD' need to use hash
    event_name: str 
    course_key: str 
    location: str 
    course: str 
    latitude: Union[confloat(ge=-90, le=90), str]
    longitude: Union[confloat(ge=-180, le=180), str]
    start_date: date 
    tour: Optional[str] = None
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.event_id, self.course_key, self.event_name))

class TourSchedulesModel(BaseModel):
    current_season: int
    schedule: Set[EventModel]
    tour: str 
    

class PlayerFieldUpdateModel(BaseModel):
    am: bool
    country: str 
    course: str 
    dg_id: int 
    dk_id: str 
    dk_salary: int 
    early_late: bool  # early is 1 
    fd_id: str 
    fd_salary: int 
    flag: str 
    pga_number: int 
    player_name: str 
    r1_teetime: Optional[str]  
    r2_teetime: Optional[str]  
    r3_teetime: Optional[str]  
    r4_teetime: Optional[str]  
    start_hole: int 
    unofficial: int 
    yh_id: str 
    yh_salary: int  
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.course))
    

class PlayerFieldUpdatesModel(BaseModel):
    current_round: int 
    event_name: str 
    field: List[PlayerFieldUpdateModel]
    last_updated: str 
    
    
class PlayerRankModel(BaseModel):
    am: bool
    country: str 
    datagolf_rank: int 
    dg_id: int
    dg_skill_estimate: float 
    owgr_rank: int 
    player_name: str 
    primary_tour: str 
    
class PreTournamentPredModel(BaseModel):
    am: bool
    country: str 
    dg_id: int
    make_cut: float 
    player_name: str 
    sample_size: int 
    top_10: float 
    top_20: float
    top_5: float
    win: float 
    
    