from collections import OrderedDict
from typing import List, Union, Optional
from datetime import datetime, timedelta

from .request import RequestHandler
from .models import PlayerFieldUpdatesModel, PlayerFieldUpdateModel, PlayerModel

CACHE_REFRESH_LABEL = 'last_refresh' # use cache object later 


class DgAPI:
    
    def __init__(self, api_key: str = None):
            
        self.request = RequestHandler(api_key=api_key) 
        self._cache = {}
            # mainly for tests w/ many repetitive api calls
            # TODO need to keep track of args to see if args change across calls in which case refresh needed
            # cache object (class) ? 
        self.cache_interval = 2  # property and setter ? should be internal ?  
             
    def refresh(self, endpoints):
        #  TODO refesh endpoints in cache
        pass 
    
    def _check_cache(self, endpoint_func, **kwargs):
        endpoint_name = endpoint_func.__name__
        if not self._cache.get(endpoint_name):
            self._cache[endpoint_name] = endpoint_func(**kwargs) 
            self._cache[CACHE_REFRESH_LABEL] = datetime.now()
        
        if self._cache.get(CACHE_REFRESH_LABEL) and (
            (datetime.now() - self._cache.get(CACHE_REFRESH_LABEL)) > timedelta(minutes=self.cache_interval)
        ): self._cache[endpoint_name] = endpoint_func(**kwargs) 
    
    @staticmethod
    def _filter_dg_objects(
        list_data, # required / must have names an ids 
        #model_type, # type to apply on list items 
        dg_id: Optional[Union[int, List[int]]] = None, 
        name: Optional[Union[str, List[str]]] = None,
    ) -> List[dict]:
        
        if all(not param for param in (dg_id, name)):
            return list_data 
    
        def match_dg_id(dg_object):
            if isinstance(dg_id, list):
                return dg_object.dg_id in [int(id_) for id_ in dg_id]
            elif dg_id is not None:
                return dg_object.dg_id == int(dg_id)
            return True
        
        def match_name(dg_object):
            player_name_lower = dg_object.player_name.lower()
            if isinstance(name, list):
                return any(all(n.lower() in player_name_lower for n in split_name) for split_name in (n.split() for n in name))
            elif name is not None:
                split_name = name.lower().split()
                return all(n in player_name_lower for n in split_name)
            return True
        
        matched_objects = set()
    
        if dg_id:
            for dg_object in list_data:
                if match_dg_id(dg_object):
                    matched_objects.add(dg_object.dg_id)
        
        if name:
            for dg_object in list_data:
                if match_name(dg_object):
                    matched_objects.add(dg_object.dg_id)
        
        filtered_objects = [player for player in list_data if player.dg_id in matched_objects]
        
        return filtered_objects
    
    def get_players(
        self,      
        dg_id: Optional[Union[int, List[int]]] = None, 
        name: Optional[Union[str, List[str]]] = None,
        **kwargs
    ) -> List[dict]:
        
        self._check_cache(self.request.player_list, **kwargs)
        
        players = [PlayerModel(**player) for player in self._cache['player_list']]
        return DgAPI._filter_dg_objects(list_data=players, name=name, dg_id=dg_id)
    
    def get_player_field_updates(self, dg_id: int = 0, dg_ids: List[int] = [], 
                                 name: str = '', names: List[str] = [], tour: str = 'pga') -> PlayerFieldUpdatesModel:

        player_field_updates: PlayerFieldUpdatesModel = self._request_handler.field_updates(tour=tour)
        player_field_updates['field'] = [PlayerFieldUpdateModel(**field_update) for field_update in player_field_updates.get('field')]
        
        if all(not _ for _ in (dg_id, dg_ids, name, names)):
            return player_field_updates
        
        target_data: List[PlayerFieldUpdateModel] = []
        dg_ids = [*dg_ids, dg_id] if dg_id else dg_ids
        names = [*names, name] if name  else names
        for player_field_update in player_field_updates['field']:
            for dg_id in dg_ids:
                if dg_id == player_field_update.dg_id:
                    target_data.append(player_field_update)
            for name_ in names:
                if name_comparison(name=player_field_update.player_name, target_name=name_): target_data.append(player_field_update)
        
        player_field_updates['field'] = list(OrderedDict.fromkeys(target_data))         
        return player_field_updates   

    def get_current_tournament(self, **kwargs) -> dict:
        return {k: v for k, v in self.request.field_updates(**kwargs).items() if k == 'event_name'}

    def get_current_round(self, **kwargs) -> dict:
        return {k: v for k, v in self.request.field_updates(**kwargs).items() if k == 'current_round'}
    
    def get_player_live_stats(): pass 
    
    def get_player_live_score(): pass 
    
    def get_player_live_predictions(): pass 
    
    def get_player_combined_stats_predictions(): pass 
    
    def get_dg_rankings_amateurs(): pass
    
    def get_leaderboard(size: int = 25, tour: str = 'pga'): pass
    

    '''
    def get_player_live_stats(self, names: list, **kwargs) -> dict:
        """stats should be a string comma separated list
           i.e. stats='sg_putt,sg_app'
        """
        if 'stats' in kwargs.keys():
            assert ' ' not in kwargs['stats'], "stats should not have spaces. i.e. stats='sg_putt,sg_app'"
        return self._general_filtered_get(request_func=self._request_handler.get_live_stats,
                                          exception_field='live_stats',
                                          names=names, **kwargs)
    '''