from datetime import datetime, timedelta
import copy 
from typing import (
    List, 
    Dict,
    Union, 
    Optional,
    Any,
) 

from .request import RequestHandler
from .models import *


class DgAPI:
    """TODO add docs
    """
    
    _cache_refesh_key = 'last_refresh'
    
    _base_endpoint_params = ('tour', 'file_format')
    
    def __init__(self, api_key: Optional[str] = None):
            
        self._request = RequestHandler(api_key=api_key)  # should be public ? 
        self._cache = {}
            # mainly for tests w/ many repetitive api calls
            # TODO need to keep track of kwargs to see if args change across calls in which case refresh needed
            # cache object (class) ? 
        self.cache_interval = 2  # @property ? should be internal ?  
             
    def refresh(self, endpoints):
        #  TODO refesh endpoints in cache ? 
        pass 
    
    def _check_cache(self, endpoint_func, **kwargs):
        endpoint_name = endpoint_func.__name__
        if not self._cache.get(endpoint_name):
            self._cache[endpoint_name] = endpoint_func(**kwargs) 
            self._cache[DgAPI._cache_refesh_key] = datetime.now()
        
        if self._cache.get(DgAPI._cache_refesh_key) and (
            (datetime.now() - self._cache.get(DgAPI._cache_refesh_key)) > timedelta(minutes=self.cache_interval)
        ): self._cache[endpoint_name] = endpoint_func(**kwargs) 
    
    
    @staticmethod
    def _get_valid_model_fields(model_class) -> set:
        """Get valid field names for a Pydantic model."""
        return set(model_class.model_fields.keys())
    
    @staticmethod
    def _separate_filter_fields_by_type(data: Dict[str, Union[int, str, List[Union[int, str]]]]) -> Dict[str, Dict[str, Any]]:
        
        int_fields = {}
        str_fields = {}
        
        def is_int_string(s: str) -> bool:
            try:
                int(s)
                return True
            except ValueError:
                return False

        for k, v in data.items():
            if isinstance(v, list):
                if v and isinstance(v[0], int):
                    int_fields[k] = v
                elif v and isinstance(v[0], str):
                    if is_int_string(v[0]):
                        int_fields[k] = [int(v) for v in v]
                    else:
                        str_fields[k] = v
            elif isinstance(v, int):
                int_fields[k] = v
            elif isinstance(v, str):
                if is_int_string(v):
                    int_fields[k] = int(v)
                else:
                    str_fields[k] = v
        return {
            'int_fields': int_fields,
            'str_fields': str_fields
        }
    
    @staticmethod
    def _filter_dg_objects(
        dg_objects: list, 
        **filter_fields
    ) -> set[dict]:
        
        if not filter_fields:
            return set(dg_objects)
        
        # fails if non int string is passed to a field which expects an int 
        # some event ids can be int or string; maybe convert all event_ids to int before passing here. 
        
        separated_filters = DgAPI._separate_filter_fields_by_type(filter_fields)
        
        def match_int(dg_object, misc_field: tuple):
            key = misc_field[0]
            value = misc_field[1]
            if dg_object[key] == 'TBD': return False
            if isinstance(value, list):
                return int(dg_object[key]) in [int(id_) for id_ in value]
            elif value is not None:
                return dg_object[key] == int(value)
            return True
        
        def match_string(dg_object, misc_field: tuple):
            key = misc_field[0]
            value = misc_field[1]
            misc_str_value_lower = dg_object[key].lower()
            
            if isinstance(value, list):
                return any(all(n.lower() in misc_str_value_lower for n in split_str) for split_str in (n.split() for n in value))
            elif value is not None:
                split_str = value.lower().split()
                return all(n in misc_str_value_lower for n in split_str)
            return True
            
        matched_objects = set()
        
        for k, v in separated_filters['int_fields'].items():
            for dg_object in dg_objects:
                # TODO maybe don't pass tuple for misc_field
                if match_int(dg_object, (k,v)): matched_objects.add(dg_object)
                        
        for k, v in separated_filters['str_fields'].items():
            for dg_object in dg_objects:
                if match_string(dg_object, (k,v)): matched_objects.add(dg_object)
        
        return matched_objects
            
    def get_players(
        self,      
        **kwargs
    ) -> set[Player]:
        # TODO all endpoint use file_format, no need to specify here. 
        endpoint_fields = ('file_format')
        
        # TODO move this logic elsewhere since used a lot. 
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        # Filter out invalid field names to handle gracefully
        valid_fields = self._get_valid_model_fields(Player)
        filter_fields = {k: v for k, v in filter_fields.items() if k in valid_fields}
        
        endpoint = self._request.player_list
        self._check_cache(endpoint, **kwargs)     
        
        player_models = [Player(**player) for player in self._cache[endpoint.__name__]]
        
        # If no filter fields remain after validation, return all players as a set
        if not filter_fields:
            return set(player_models)
        
        return DgAPI._filter_dg_objects(dg_objects=player_models, **filter_fields)
    
    # TODO  to parse kwargs and assign endpoint fields based on lookup 
    # keep in mind nested lists need deep copy from cache
    def get_player_field_updates(
        self,
        **kwargs
    ) -> PlayerFieldUpdates:
        endpoint_fields = DgAPI._base_endpoint_params
        
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        endpoint = self._request.field_updates
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['field'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerFieldUpdate(**update) for update in data['field']], 
            **filter_fields
        )
        return PlayerFieldUpdates(**data)

    def get_current_tournament(self, **kwargs) -> Dict[str, str]:
        # TODO for this method and next. Specify tour in returned struct.
        endpoint = self._request.field_updates
        self._check_cache(endpoint, **kwargs)
        return {k: v for k, v in self._cache[endpoint.__name__].items() if k == 'event_name'}

    def get_current_round(self, **kwargs) -> Dict[str, int]:
        endpoint = self._request.field_updates
        self._check_cache(endpoint, **kwargs)
        return {k: v for k, v in self._cache[endpoint.__name__].items() if k == 'current_round'}
    
    def get_tour_schedules(
        self,
        **kwargs
    ) -> TourSchedules: 
        endpoint_fields = DgAPI._base_endpoint_params
    
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        
        endpoint = self._request.tour_schedules
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])      

        data['schedule'] = DgAPI._filter_dg_objects(
            dg_objects=[Event(**event) for event in data['schedule']], 
            **filter_fields
        )
        return TourSchedules(**data)
    
    def get_live_hole_scoring_distributions(
        self,
        **kwargs
    ) -> LiveHoleScoringDistributions: 
        """potential params 
            morning, afternoon 
            round num 
            tournament -> course 
                i think endpoint can return more than one course
        """
        
        endpoint_fields = DgAPI._base_endpoint_params
        
        endpoint = self._request.live_hole_scoring_distributions 
        self._check_cache(endpoint, **kwargs)
        
        data =copy.deepcopy(self._cache[endpoint.__name__]) 
    
        for course in data['courses']:
            for round_data in course['rounds']:
                for hole in round_data['holes']:
                    for k, v in hole.items():
                        if 'wave' in k or k == 'total':
                            hole[k] = LiveHoleScoringWaveData(**v)
                    hole.update(LiveHoleScoringHoleData(**hole).model_dump())
                round_data.update(LiveHoleScoringRoundData(**round_data).model_dump())
            course.update(LiveHoleScoringCourseData(**course).model_dump())
        return LiveHoleScoringDistributions(**data)
        
        

    def get_avg_score_per_hole():
        """
            morning, afternoon 
            round num default to all -> I might have to avg them all manually, api doesn't do it it appears
            course
        """
        pass 
    def get_player_live_stats(): pass 
    
    def get_player_live_score(): pass 
    
    def get_dg_rankings_amateurs(): pass
    
    def get_data_golf_rankings(self, **kwargs) -> DataGolfRankings:
        """Returns the top 500 players in the current DG rankings."""
        endpoint_fields = ('file_format',)
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.data_golf_rankings
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['rankings'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerRanking(**ranking) for ranking in data['rankings']],
            **filter_fields
        )
        return DataGolfRankings(**data)
    
    def get_pre_tournament_predictions(self, **kwargs) -> PreTournamentPredictions:
        """Returns full-field probabilistic forecasts for upcoming tournaments."""
        endpoint_fields = ('tour', 'add_position', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.pre_tournament_predictions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        if 'baseline' in data:
            data['baseline'] = DgAPI._filter_dg_objects(
                dg_objects=[BaselinePrediction(**pred) for pred in data['baseline']],
                **filter_fields
            )
        if 'baseline_history_fit' in data:
            data['baseline_history_fit'] = DgAPI._filter_dg_objects(
                dg_objects=[BaselineHistoryFitPrediction(**pred) for pred in data['baseline_history_fit']],
                **filter_fields
            )
        return PreTournamentPredictions(**data)
    
    def get_pre_tournament_predictions_archive(self, **kwargs) -> PreTournamentPredictionsArchive:
        """Returns historical PGA Tour pre-tournament predictions."""
        endpoint_fields = ('event_id', 'year', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.pre_tournament_predictions_archive
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        if 'baseline' in data:
            data['baseline'] = DgAPI._filter_dg_objects(
                dg_objects=[BaselinePredictionArchive(**pred) for pred in data['baseline']],
                **filter_fields
            )
        if 'baseline_history_fit' in data:
            data['baseline_history_fit'] = DgAPI._filter_dg_objects(
                dg_objects=[BaselineHistoryFitPredictionArchive(**pred) for pred in data['baseline_history_fit']],
                **filter_fields
            )
        return PreTournamentPredictionsArchive(**data)
    
    def get_player_skill_decompositions(self, **kwargs) -> PlayerSkillDecompositions:
        """Returns detailed strokes-gained breakdown for players."""
        endpoint_fields = ('tour', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.player_skill_decompositions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['players'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerSkillDecomposition(**player) for player in data['players']],
            **filter_fields
        )
        return PlayerSkillDecompositions(**data)
    
    def get_player_skill_ratings(self, **kwargs) -> PlayerSkillRatings:
        """Returns skill estimates and ranks for all players."""
        endpoint_fields = ('display', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.player_skill_ratings
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['players'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerSkillRating(**player) for player in data['players']],
            **filter_fields
        )
        return PlayerSkillRatings(**data)
    
    def get_detailed_approach_skill(self, **kwargs) -> DetailedApproachSkill:
        """Returns detailed approach performance stats by yardage/lie buckets."""
        endpoint_fields = ('period', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.detailed_approach_skill
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['data'] = DgAPI._filter_dg_objects(
            dg_objects=[ApproachSkillData(**item) for item in data['data']],
            **filter_fields
        )
        return DetailedApproachSkill(**data)
    
    def get_live_model_predictions(self, **kwargs) -> LiveModelPredictions:
        """Returns live finish probabilities for ongoing tournaments."""
        endpoint_fields = ('tour', 'dead_heat', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.live_model_predictions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['data'] = DgAPI._filter_dg_objects(
            dg_objects=[LivePrediction(**pred) for pred in data['data']],
            **filter_fields
        )
        return LiveModelPredictions(**data)
    
    def get_live_tournament_stats(self, **kwargs) -> LiveTournamentStats:
        """Returns live strokes-gained and traditional stats for PGA Tour Events."""
        endpoint_fields = ('stats', 'round', 'display', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.live_tournament_stats
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['live_stats'] = DgAPI._filter_dg_objects(
            dg_objects=[LiveStat(**stat) for stat in data['live_stats']],
            **filter_fields
        )
        return LiveTournamentStats(**data)
    
    def get_fantasy_projection_defaults(self, **kwargs) -> FantasyProjectionDefaults:
        """Returns default fantasy projections for DFS contests."""
        endpoint_fields = ('tour', 'site', 'slate', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.fantasy_projection_defaults
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['projections'] = DgAPI._filter_dg_objects(
            dg_objects=[FantasyProjection(**proj) for proj in data['projections']],
            **filter_fields
        )
        return FantasyProjectionDefaults(**data)
    
    def get_outright_odds(self, **kwargs) -> OutrightOdds:
        """Returns sportsbook odds comparison for tournament winners and finishes."""
        endpoint_fields = ('tour', 'market', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.outright_odds
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        for odd in data['odds']:
            odd['datagolf'] = DataGolfOdds(**odd['datagolf'])
        
        data['odds'] = DgAPI._filter_dg_objects(
            dg_objects=[OutrightOdd(**odd) for odd in data['odds']],
            **filter_fields
        )
        return OutrightOdds(**data)
    
    def get_matchup_odds(self, **kwargs) -> dict:
        """Returns tournament and round matchup odds from sportsbooks."""
        endpoint_fields = ('tour', 'market', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.matchup_odds
        self._check_cache(endpoint, **kwargs)
        
        # Note: matchup_odds returns variable structure, sometimes just string message
        data = self._cache[endpoint.__name__]
        return data
    
    def get_matchup_odds_all_pairings(self, **kwargs) -> MatchupOddsAllPairings:
        """Returns Data Golf generated matchup odds for all possible pairings."""
        endpoint_fields = ('tour', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.matchup_odds_all_pairings
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        pairings = []
        for pairing in data['pairings']:
            pairings.append(MatchupPairing(
                course=pairing['course'],
                group=pairing['group'],
                p1=PlayerPairing(**pairing['p1']),
                p2=PlayerPairing(**pairing['p2']),
                p3=PlayerPairing(**pairing['p3']),
                start_hole=pairing['start_hole'],
                teetime=pairing['teetime']
            ))
        
        data['pairings'] = DgAPI._filter_dg_objects(dg_objects=pairings, **filter_fields)
        return MatchupOddsAllPairings(**data)
    
    def get_historical_raw_data_event_ids(self, **kwargs) -> List[HistoricalRawDataEvent]:
        """Returns event IDs for historical raw data across tours."""
        endpoint_fields = ('tour', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_raw_data_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        return DgAPI._filter_dg_objects(
            dg_objects=[HistoricalRawDataEvent(**event) for event in data],
            **filter_fields
        )
    
    def get_historical_round_scoring_data(self, **kwargs) -> HistoricalRoundScoringData:
        """Returns detailed round-by-round scoring and strokes gained data."""
        endpoint_fields = ('tour', 'event_id', 'year', 'round', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_round_scoring_data
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        # Process scores with round data
        scores = []
        for score in data['scores']:
            round_data = {}
            for round_key in ['round_1', 'round_2', 'round_3', 'round_4']:
                if round_key in score and score[round_key]:
                    round_data[round_key] = RoundStats(**score[round_key])
                else:
                    round_data[round_key] = None
            
            scores.append(PlayerRoundScore(
                dg_id=score['dg_id'],
                fin_text=score['fin_text'],
                player_name=score['player_name'],
                **round_data
            ))
        
        data['scores'] = DgAPI._filter_dg_objects(dg_objects=scores, **filter_fields)
        return HistoricalRoundScoringData(**data)
    
    def get_historical_odds_event_ids(self, **kwargs) -> List[HistoricalOddsEvent]:
        """Returns event IDs for historical betting odds data."""
        endpoint_fields = ('tour', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_odds_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        return DgAPI._filter_dg_objects(
            dg_objects=[HistoricalOddsEvent(**event) for event in data],
            **filter_fields
        )
    
    def get_historical_outright_odds(self, **kwargs) -> HistoricalOutrightOdds:
        """Returns opening and closing lines for various betting markets."""
        endpoint_fields = ('tour', 'event_id', 'year', 'market', 'book', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_outright_odds
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['odds'] = DgAPI._filter_dg_objects(
            dg_objects=[HistoricalOutrightOdd(**odd) for odd in data['odds']],
            **filter_fields
        )
        return HistoricalOutrightOdds(**data)
    
    def get_historical_matchup_odds(self, **kwargs) -> HistoricalMatchupOdds:
        """Returns historical matchup and 3-ball betting odds."""
        endpoint_fields = ('tour', 'event_id', 'year', 'market', 'book', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_matchup_odds
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['odds'] = DgAPI._filter_dg_objects(
            dg_objects=[HistoricalMatchupOdd(**odd) for odd in data['odds']],
            **filter_fields
        )
        return HistoricalMatchupOdds(**data)
    
    def get_historical_dfs_event_ids(self, **kwargs) -> List[HistoricalDfsEvent]:
        """Returns event IDs for historical DFS data."""
        endpoint_fields = ('tour', 'site', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_dfs_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        return DgAPI._filter_dg_objects(
            dg_objects=[HistoricalDfsEvent(**event) for event in data],
            **filter_fields
        )
    
    def get_historical_dfs_points_salaries(self, **kwargs) -> HistoricalDfsPointsSalaries:
        """Returns DFS points, salaries, and ownership percentages."""
        endpoint_fields = ('tour', 'site', 'event_id', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_dfs_points_salaries
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['dfs_points'] = DgAPI._filter_dg_objects(
            dg_objects=[DfsPlayerPoints(**points) for points in data['dfs_points']],
            **filter_fields
        )
        return HistoricalDfsPointsSalaries(**data)
    
    def get_leaderboard(self, size: int = 200, **kwargs) -> List[LeaderboardItem]:
        """Extract leaderboard from live tournament stats."""
        stats_data = self.get_live_tournament_stats(**kwargs)
        return LeaderBoard(
            course_name=stats_data.course_name,
            event_name=stats_data.event_name,
            last_updated=stats_data.last_updated, 
            items=[LeaderboardItem(
                player_name=data.player_name,
                dg_id=data.dg_id,
                position=data.position,
                thru=data.thru,
                total=data.total
            ) for data in stats_data.live_stats[:size]]
        )
    
    def get_player_live_stats(self, player_id: int, **kwargs) -> Optional[LiveStat]:
        """Extract specific player from live tournament stats for the PGA tour."""
        stats_data = self.get_live_tournament_stats(**kwargs)
        for player in stats_data.live_stats:
            if player.dg_id == player_id:
                return player
        return None
    
    def get_player_live_score(self, player_id: int, **kwargs) -> Optional[Dict[str, Union[str, int, float]]]:
        """Extract player position/score from live model predictions."""
        predictions_data = self.get_live_model_predictions(**kwargs)
        for player in predictions_data.data:
            if player.dg_id == player_id:
                return {
                    'position': player.current_pos,
                    'score': player.current_score,
                    'player_name': player.player_name,
                    'win_prob': player.win
                }
        return None
    
    def get_dg_rankings_amateurs(self, **kwargs) -> List[PlayerRanking]:
        """Filter amateur players from data golf rankings."""
        rankings_data = self.get_data_golf_rankings(**kwargs)
        return [player for player in rankings_data.rankings if player.am == 1]