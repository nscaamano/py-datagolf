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
from .models import (
    PlayerModel,
    PlayerFieldUpdateModel,
    PlayerFieldUpdatesModel,
    TourSchedulesModel,
    EventModel,
    LiveHoleScoringDistributions,
    LiveHoleScoringCourseData,
    LiveHoleScoringRoundData,
    LiveHoleScoringHoleData,
    LiveHoleScoringWaveData,
)


class DgAPI:
    """TODO add docs
    """
    
    _cache_refesh_key = 'last_refresh'
    
    _base_endpoint_fields = ('tour', 'file_format')
    
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
    ) -> list[dict]:
        
        if not filter_fields:
            return dg_objects
        
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
    ) -> List[PlayerModel]:
        # TODO all endpoint use file_format, no need to specify here. 
        endpoint_fields = ('file_format')
        
        # TODO move this logic elsewhere since used a lot. 
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        endpoint = self._request.player_list
        self._check_cache(endpoint, **kwargs)     
        
        return DgAPI._filter_dg_objects(
            dg_objects=[PlayerModel(**player) for player in self._cache[endpoint.__name__]], 
            **filter_fields
        )
    
    # TODO decorator to parse kwargs and assign endpoint fields based on lookup 
    # keep in mind nested lists need deep copy from cache
    def get_player_field_updates(
        self,
        **kwargs
    ) -> PlayerFieldUpdatesModel:
        endpoint_fields = DgAPI._base_endpoint_fields
        
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        endpoint = self._request.field_updates
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        
        data['field'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerFieldUpdateModel(**update) for update in data['field']], 
            **filter_fields
        )
        return PlayerFieldUpdatesModel(**data)

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
    ) -> TourSchedulesModel: 
        endpoint_fields = DgAPI._base_endpoint_fields
    
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        
        endpoint = self._request.tour_schedules
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])      

        data['schedule'] = DgAPI._filter_dg_objects(
            dg_objects=[EventModel(**event) for event in data['schedule']], 
            **filter_fields
        )
        return TourSchedulesModel(**data)
    
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
        
        endpoint_fields = DgAPI._base_endpoint_fields
        
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
    
    def get_data_golf_rankings(self, **kwargs) -> dict:
        """Returns the top 500 players in the current DG rankings."""
        endpoint_fields = ('file_format',)
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.data_golf_rankings
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'rankings' in data:
            data['rankings'] = DgAPI._filter_dg_objects(dg_objects=data['rankings'], **filter_fields)
        return data
    
    def get_pre_tournament_predictions(self, **kwargs) -> dict:
        """Returns full-field probabilistic forecasts for upcoming tournaments."""
        endpoint_fields = ('tour', 'add_position', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.pre_tournament_predictions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields:
            if 'baseline' in data:
                data['baseline'] = DgAPI._filter_dg_objects(dg_objects=data['baseline'], **filter_fields)
            if 'baseline_history_fit' in data:
                data['baseline_history_fit'] = DgAPI._filter_dg_objects(dg_objects=data['baseline_history_fit'], **filter_fields)
        return data
    
    def get_pre_tournament_predictions_archive(self, **kwargs) -> dict:
        """Returns historical PGA Tour pre-tournament predictions."""
        endpoint_fields = ('event_id', 'year', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.pre_tournament_predictions_archive
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields:
            if 'baseline' in data:
                data['baseline'] = DgAPI._filter_dg_objects(dg_objects=data['baseline'], **filter_fields)
            if 'baseline_history_fit' in data:
                data['baseline_history_fit'] = DgAPI._filter_dg_objects(dg_objects=data['baseline_history_fit'], **filter_fields)
        return data
    
    def get_player_skill_decompositions(self, **kwargs) -> dict:
        """Returns detailed strokes-gained breakdown for players."""
        endpoint_fields = ('tour', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.player_skill_decompositions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'players' in data:
            data['players'] = DgAPI._filter_dg_objects(dg_objects=data['players'], **filter_fields)
        return data
    
    def get_player_skill_ratings(self, **kwargs) -> dict:
        """Returns skill estimates and ranks for all players."""
        endpoint_fields = ('display', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.player_skill_ratings
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'players' in data:
            data['players'] = DgAPI._filter_dg_objects(dg_objects=data['players'], **filter_fields)
        return data
    
    def get_detailed_approach_skill(self, **kwargs) -> dict:
        """Returns detailed approach performance stats by yardage/lie buckets."""
        endpoint_fields = ('period', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.detailed_approach_skill
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'data' in data:
            data['data'] = DgAPI._filter_dg_objects(dg_objects=data['data'], **filter_fields)
        return data
    
    def get_live_model_predictions(self, **kwargs) -> dict:
        """Returns live finish probabilities for ongoing tournaments."""
        endpoint_fields = ('tour', 'dead_heat', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.live_model_predictions
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'data' in data:
            data['data'] = DgAPI._filter_dg_objects(dg_objects=data['data'], **filter_fields)
        return data
    
    def get_live_tournament_stats(self, **kwargs) -> dict:
        """Returns live strokes-gained and traditional stats."""
        endpoint_fields = ('stats', 'round', 'display', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.live_tournament_stats
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'live_stats' in data:
            data['live_stats'] = DgAPI._filter_dg_objects(dg_objects=data['live_stats'], **filter_fields)
        return data
    
    def get_fantasy_projection_defaults(self, **kwargs) -> dict:
        """Returns default fantasy projections for DFS contests."""
        endpoint_fields = ('tour', 'site', 'slate', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.fantasy_projection_defaults
        self._check_cache(endpoint, **kwargs)
        
        data = copy.deepcopy(self._cache[endpoint.__name__])
        if filter_fields and 'projections' in data:
            data['projections'] = DgAPI._filter_dg_objects(dg_objects=data['projections'], **filter_fields)
        return data
    
    def get_outright_odds(self, **kwargs) -> List[dict]:
        """Returns sportsbook odds comparison for tournament winners and finishes."""
        endpoint_fields = ('tour', 'market', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.outright_odds
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_matchup_odds(self, **kwargs) -> List[dict]:
        """Returns tournament and round matchup odds from sportsbooks."""
        endpoint_fields = ('tour', 'market', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.matchup_odds
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_matchup_odds_all_pairings(self, **kwargs) -> List[dict]:
        """Returns Data Golf generated matchup odds for all possible pairings."""
        endpoint_fields = ('tour', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.matchup_odds_all_pairings
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_raw_data_event_ids(self, **kwargs) -> List[dict]:
        """Returns event IDs for historical raw data across tours."""
        endpoint_fields = ('tour', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_raw_data_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_round_scoring_data(self, **kwargs) -> List[dict]:
        """Returns detailed round-by-round scoring and strokes gained data."""
        endpoint_fields = ('tour', 'event_id', 'year', 'round', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_round_scoring_data
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_odds_event_ids(self, **kwargs) -> List[dict]:
        """Returns event IDs for historical betting odds data."""
        endpoint_fields = ('tour', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_odds_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_outright_odds(self, **kwargs) -> List[dict]:
        """Returns opening and closing lines for various betting markets."""
        endpoint_fields = ('tour', 'event_id', 'year', 'market', 'book', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_outright_odds
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_matchup_odds(self, **kwargs) -> List[dict]:
        """Returns historical matchup and 3-ball betting odds."""
        endpoint_fields = ('tour', 'event_id', 'year', 'market', 'book', 'odds_format', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_matchup_odds
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_dfs_event_ids(self, **kwargs) -> List[dict]:
        """Returns event IDs for historical DFS data."""
        endpoint_fields = ('tour', 'site', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_dfs_event_ids
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_historical_dfs_points_salaries(self, **kwargs) -> List[dict]:
        """Returns DFS points, salaries, and ownership percentages."""
        endpoint_fields = ('tour', 'site', 'event_id', 'year', 'file_format')
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields}
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields}
        
        endpoint = self._request.historical_dfs_points_salaries
        self._check_cache(endpoint, **kwargs)
        
        data = self._cache[endpoint.__name__]
        if filter_fields:
            return DgAPI._filter_dg_objects(dg_objects=data, **filter_fields)
        return data
    
    def get_leaderboard(self, size: int = 25, tour: str = 'pga', **kwargs) -> List[dict]:
        """Extract leaderboard from live tournament stats."""
        stats_data = self.get_live_tournament_stats(tour=tour, **kwargs)
        if isinstance(stats_data, dict) and 'live_stats' in stats_data:
            return stats_data['live_stats'][:size]
        return []
    
    def get_player_live_stats(self, player_id: int, **kwargs) -> dict:
        """Extract specific player from live tournament stats."""
        stats_data = self.get_live_tournament_stats(**kwargs)
        if isinstance(stats_data, dict) and 'live_stats' in stats_data:
            for player in stats_data['live_stats']:
                if player.get('dg_id') == player_id or player.get('player_id') == player_id:
                    return player
        return {}
    
    def get_player_live_score(self, player_id: int, **kwargs) -> dict:
        """Extract player position/score from live model predictions."""
        predictions_data = self.get_live_model_predictions(**kwargs)
        if isinstance(predictions_data, dict) and 'data' in predictions_data:
            for player in predictions_data['data']:
                if player.get('dg_id') == player_id or player.get('player_id') == player_id:
                    return {
                        'position': player.get('current_pos'),
                        'score': player.get('current_score'),
                        'player_name': player.get('player_name'),
                        'win_prob': player.get('win')
                    }
        return {}
    
    def get_dg_rankings_amateurs(self, **kwargs) -> List[dict]:
        """Filter amateur players from data golf rankings."""
        rankings_data = self.get_data_golf_rankings(**kwargs)
        if isinstance(rankings_data, dict) and 'rankings' in rankings_data:
            return [player for player in rankings_data['rankings'] if player.get('am') == 1]
        return []