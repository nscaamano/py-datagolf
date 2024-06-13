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
)


class DgAPI:
    """TODO add docs
    """
    
    _cache_refesh_key = 'last_refresh'
    
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
        endpoint_fields = ['file_format']
        
        # TODO move this logic elsewhere since used a lot. 
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        endpoint = self._request.player_list
        self._check_cache(endpoint, **kwargs)
        
        # TODO test if this is necessary here as well. Noticed issue with tour schedules filtering cache as well.
        # perhaps because nested dict in schedules model 
        players = copy.deepcopy(self._cache[endpoint.__name__])      
        
        return DgAPI._filter_dg_objects(
            dg_objects=[PlayerModel(**player) for player in self._cache[endpoint.__name__]], 
            **filter_fields
        )
    
    # TODO decorator to parse kwargs and assign endpoint fields based on lookup 
    def get_player_field_updates(
        self,
        **kwargs
    ) -> PlayerFieldUpdatesModel:
        endpoint_fields = ['tour', 'file_format']
        
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        endpoint = self._request.field_updates
        self._check_cache(endpoint, **kwargs)
        
        update = copy.deepcopy(self._cache[endpoint.__name__])
        
        update['field'] = DgAPI._filter_dg_objects(
            dg_objects=[PlayerFieldUpdateModel(**update) for update in update['field']], 
            **filter_fields
        )
        return PlayerFieldUpdatesModel(**update)

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
        endpoint_fields = ['file_format', 'tour']  # look up somewhere ? different for each get method
    
        filter_fields = {k: v for k,v in kwargs.items() if k not in endpoint_fields }
        kwargs = {k: v for k,v in kwargs.items() if k in endpoint_fields }
        
        
        endpoint = self._request.tour_schedules
        self._check_cache(endpoint, **kwargs)
        
        tour_schedules = copy.deepcopy(self._cache[endpoint.__name__])      

        tour_schedules['schedule'] = DgAPI._filter_dg_objects(
            dg_objects=[EventModel(**event) for event in tour_schedules['schedule']], 
            **filter_fields
        )
        return TourSchedulesModel(**tour_schedules)
    '''
    def get_live_hole_scoring_distributions(
        self,
        **kwargs
    ) -> PlaceHolder: 
        pass 
    '''
    
    def get_player_live_stats(): pass 
    
    def get_player_live_score(): pass 
    
    def get_dg_rankings_amateurs(): pass
    
    def get_leaderboard(size: int = 25, tour: str = 'pga'): pass