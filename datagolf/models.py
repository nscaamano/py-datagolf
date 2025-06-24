from pydantic import BaseModel, confloat, conint, Field, ConfigDict
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
    
    
# Data Golf Rankings Models
class PlayerRankingModel(BaseModel):
    am: int  # 0 or 1
    country: str 
    datagolf_rank: int 
    dg_id: int
    dg_skill_estimate: float 
    owgr_rank: int 
    player_name: str 
    primary_tour: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.datagolf_rank))

class DataGolfRankingsModel(BaseModel):
    last_updated: str
    notes: str
    rankings: List[PlayerRankingModel]

# Pre-Tournament Predictions Models
class BaselinePredictionModel(BaseModel):
    am: int
    country: str 
    dg_id: int
    make_cut: float 
    player_name: str 
    sample_size: int 
    top_10: float 
    top_20: float
    top_5: float
    win: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class BaselineHistoryFitPredictionModel(BaseModel):
    am: int
    country: str 
    dg_id: int
    make_cut: float 
    player_name: str 
    sample_size: int 
    top_10: float 
    top_20: float
    top_5: float
    win: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class PreTournamentPredictionsModel(BaseModel):
    baseline: List[BaselinePredictionModel]
    baseline_history_fit: List[BaselineHistoryFitPredictionModel]
    dead_heats: str
    event_name: str
    last_updated: str
    models_available: List[str] 
    
class LiveHoleScoringWaveData(BaseModel):
    avg_score: Optional[float] 
    birdies: int 
    bogeys: int 
    doubles_or_worse: int 
    eagles_or_better: int 
    pars: int 
    players_thru: int 
    
class LiveHoleScoringHoleData(BaseModel):
    afternoon_wave: LiveHoleScoringWaveData 
    hole: int 
    morning_wave: LiveHoleScoringWaveData 
    par: int
    total: LiveHoleScoringWaveData 
    yardage: int
    
class LiveHoleScoringRoundData(BaseModel):
    holes: List[LiveHoleScoringHoleData] 
    round_num: int 

    
class LiveHoleScoringCourseData(BaseModel):
    course_code: str 
    course_key: str
    rounds: List[LiveHoleScoringRoundData] 
    
class LiveHoleScoringDistributions(BaseModel):
    courses: List[LiveHoleScoringCourseData]
    current_round: int
    event_name: str 
    last_update: str

# Pre-Tournament Predictions Archive Models
class BaselinePredictionArchiveModel(BaseModel):
    dg_id: int
    fin_text: str
    first_round_leader: float
    make_cut: float
    player_name: str
    top_10: float
    top_20: float
    top_3: float
    top_30: float
    top_5: float
    win: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class BaselineHistoryFitPredictionArchiveModel(BaseModel):
    dg_id: int
    fin_text: str
    first_round_leader: float
    make_cut: float
    player_name: str
    top_10: float
    top_20: float
    top_3: float
    top_30: float
    top_5: float
    win: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class PreTournamentPredictionsArchiveModel(BaseModel):
    baseline: List[BaselinePredictionArchiveModel]
    baseline_history_fit: List[BaselineHistoryFitPredictionArchiveModel]
    event_completed: date
    event_id: str
    event_name: str
    models_available: List[str]

# Player Skill Decompositions Models
class PlayerSkillDecompositionModel(BaseModel):
    age: int
    age_adjustment: float
    am: int
    baseline_pred: float
    cf_approach_comp: float
    cf_short_comp: float
    country: str
    course_experience_adjustment: float
    course_history_adjustment: float
    dg_id: int
    player_name: str
    # Note: Many more fields exist but truncated in sample data
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class PlayerSkillDecompositionsModel(BaseModel):
    course_name: str
    event_name: str
    last_updated: str
    notes: str
    players: List[PlayerSkillDecompositionModel]

# Player Skill Ratings Models
class PlayerSkillRatingModel(BaseModel):
    dg_id: int
    driving_acc: float
    driving_dist: float
    player_name: str
    sg_app: float
    sg_arg: float
    sg_ott: float
    sg_putt: float
    sg_total: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class PlayerSkillRatingsModel(BaseModel):
    last_updated: str
    players: List[PlayerSkillRatingModel]

# Detailed Approach Skill Models
class ApproachSkillDataModel(BaseModel):
    # Note: This model has many yardage/lie specific fields
    # Sample fields from fixture data
    dg_id: Optional[int] = None
    player_name: Optional[str] = None
    # Add more fields as needed from actual data
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name)) if self.dg_id and self.player_name else hash(id(self))

class DetailedApproachSkillModel(BaseModel):
    data: List[ApproachSkillDataModel]
    last_updated: str
    time_period: str

# Live Model Predictions Models
class LivePredictionModel(BaseModel):
    R1: Optional[int]
    R2: Optional[int]
    R3: Optional[int]
    R4: Optional[int]
    country: str
    course: str
    current_pos: str
    current_score: int
    dg_id: int
    end_hole: int
    make_cut: float
    player_name: str
    round: int
    thru: int
    today: int
    top_10: float
    top_20: float
    top_5: float
    win: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class LiveModelPredictionsModel(BaseModel):
    data: List[LivePredictionModel]
    info: dict  # Info structure varies

# Live Tournament Stats Models
class LiveStatModel(BaseModel):
    course: Optional[str]        # null for withdrawn players
    dg_id: int
    player_name: str
    position: str                # Shows "WD" for withdrawn players
    round: Optional[int]         # null for withdrawn players
    sg_app: Optional[float]      # null for withdrawn players
    sg_arg: Optional[float]      # null for withdrawn players
    sg_ott: Optional[float]      # null for withdrawn players
    sg_putt: Optional[float]     # null for withdrawn players
    sg_t2g: Optional[float]      # null for withdrawn players
    sg_total: Optional[float]    # null for withdrawn players
    thru: Optional[int]          # null for withdrawn players
    total: Optional[int]         # null for withdrawn players
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class LiveTournamentStatsModel(BaseModel):
    course_name: str
    event_name: str
    last_updated: str # TODO should these be timestamp type ?
    live_stats: List[LiveStatModel]
    stat_display: str
    stat_round: str

# Fantasy Projection Defaults Models
class FantasyProjectionModel(BaseModel):
    dg_id: int
    early_late_wave: int
    player_name: str
    proj_ownership: Optional[float]
    proj_points_finish: float
    proj_points_scoring: float
    proj_points_total: float
    r1_teetime: str
    salary: int
    site_name_id: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class FantasyProjectionDefaultsModel(BaseModel):
    event_name: str
    last_updated: str
    note: str
    projections: List[FantasyProjectionModel]
    site: str
    slate: str
    tour: str

# Betting Tools Models
class DataGolfOddsModel(BaseModel):
    """DataGolf's own odds predictions."""
    baseline: Optional[float]
    baseline_history_fit: Optional[float]

class OutrightOddModel(BaseModel):
    """Individual player's odds across all sportsbooks."""
    # Required fields that are always present
    dg_id: int
    player_name: str
    datagolf: DataGolfOddsModel
    
    # Optional sportsbook fields - these vary by availability
    bet365: Optional[float] = None
    betcris: Optional[float] = None
    betonline: Optional[float] = None
    betmgm: Optional[float] = None
    betway: Optional[float] = None
    bovada: Optional[float] = None
    caesars: Optional[float] = None
    draftkings: Optional[float] = None
    fanduel: Optional[float] = None
    pinnacle: Optional[float] = None
    skybet: Optional[float] = None
    pointsbet: Optional[float] = None
    williamhill: Optional[float] = None
    unibet: Optional[float] = None
    
    # Allow additional unknown sportsbooks
    model_config = ConfigDict(extra='allow')
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))
    
    def get_sportsbook_odds(self) -> dict:
        """Get all sportsbook odds as a dictionary, excluding DataGolf and player info."""
        exclude_fields = {'dg_id', 'player_name', 'datagolf'}
        return {k: v for k, v in self.__dict__.items() if k not in exclude_fields and v is not None}

class OutrightOddsModel(BaseModel):
    books_offering: List[str]
    event_name: str
    last_updated: str
    market: str
    #notes: Optional[str] = None  # Sometimes missing
    odds: List[OutrightOddModel]

class PlayerPairingModel(BaseModel):
    dg_id: int
    name: str
    odds: float

class MatchupPairingModel(BaseModel):
    course: str
    group: int
    p1: PlayerPairingModel
    p2: PlayerPairingModel
    p3: PlayerPairingModel
    start_hole: int
    teetime: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.group, self.p1.dg_id, self.p2.dg_id, self.p3.dg_id))

class MatchupOddsAllPairingsModel(BaseModel):
    event_name: str
    last_update: str
    pairings: List[MatchupPairingModel]
    round: int

# Historical Data Models
class HistoricalRawDataEventModel(BaseModel):
    calendar_year: int
    date: str
    event_id: int
    event_name: str
    sg_categories: str
    tour: str
    traditional_stats: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.event_id, self.calendar_year, self.tour))

class RoundStatsModel(BaseModel):
    birdies: int
    bogies: int
    course_name: str
    course_num: int
    course_par: int
    doubles_or_worse: int
    driving_acc: float
    driving_dist: float
    eagles_or_better: int
    gir: float
    great_shots: int
    pars: int
    poor_shots: int
    prox_fw: float
    prox_rgh: Optional[float]
    score: int
    scrambling: float
    # Note: Many more SG fields exist

class PlayerRoundScoreModel(BaseModel):
    dg_id: int
    fin_text: str
    player_name: str
    round_1: Optional[RoundStatsModel]
    round_2: Optional[RoundStatsModel]
    round_3: Optional[RoundStatsModel]
    round_4: Optional[RoundStatsModel]
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class HistoricalRoundScoringDataModel(BaseModel):
    event_completed: str
    event_id: str
    event_name: str
    scores: List[PlayerRoundScoreModel]
    season: int
    sg_categories: str
    tour: str
    traditional_stats: str
    year: int

class HistoricalOddsEventModel(BaseModel):
    archived_preds: str
    calendar_year: int
    event_id: int
    event_name: str
    matchups: str
    outrights: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.event_id, self.calendar_year))

class HistoricalOutrightOddModel(BaseModel):
    bet_outcome_numeric: int
    bet_outcome_text: str
    close_odds: float
    close_time: str
    dg_id: int
    open_odds: float
    open_time: str
    outcome: str
    player_name: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class HistoricalOutrightOddsModel(BaseModel):
    book: str
    event_completed: str
    event_id: str
    event_name: str
    market: str
    odds: List[HistoricalOutrightOddModel]
    season: int
    year: int

class HistoricalMatchupOddModel(BaseModel):
    bet_type: str
    close_time: str
    open_time: str
    p1_close: float
    p1_dg_id: int
    p1_open: float
    p1_outcome: float
    p1_outcome_text: str
    p1_player_name: str
    p2_close: float
    p2_dg_id: int
    p2_open: float
    p2_outcome: float
    p2_outcome_text: str
    p2_player_name: str
    p3_close: float
    p3_dg_id: int
    # Note: More p3 fields exist
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.p1_dg_id, self.p2_dg_id, self.p3_dg_id))

class HistoricalMatchupOddsModel(BaseModel):
    book: str
    event_completed: str
    event_id: str
    event_name: str
    odds: List[HistoricalMatchupOddModel]
    season: int
    year: int

class HistoricalDfsEventModel(BaseModel):
    calendar_year: int
    date: str
    dk_ownerships: str
    dk_salaries: str
    event_id: int
    event_name: str
    fd_ownerships: str
    fd_salaries: str
    tour: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.event_id, self.calendar_year, self.tour))

class DfsPlayerPointsModel(BaseModel):
    bogey_free_pts: int
    dg_id: int
    fin_text: str
    finish_pts: int
    hole_in_one_pts: int
    hole_score_pts: float
    ownership: float
    player_name: str
    salary: int
    streak_pts: int
    sub_70_pts: int
    total_pts: float
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))

class HistoricalDfsPointsSalariesModel(BaseModel):
    dfs_points: List[DfsPlayerPointsModel]
    event_completed: str
    event_id: str
    event_name: str
    ownerships_from: str
    season: int
    site: str
    tour: str
    year: int

class LeaderboardItemModel(BaseModel):
    """Individual leaderboard entry with essential player information."""
    player_name: str
    dg_id: int
    position: str
    thru: Optional[int]
    total: Optional[int]
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __hash__(self):
        return hash((self.dg_id, self.player_name))
    
class LeaderBoardModel(BaseModel):
    course_name: str
    event_name: str 
    last_updated: str 
    items: List[LeaderboardItemModel]