import json
import requests
from collections import OrderedDict

from .utils import open_json_file
from .models import Player, PlayerFieldUpdate, PlayerFieldUpdates

_ERROR = 'error'


class RequestHandler:
    """Handler for requests against the datagolf API.
    """

    _url_base = 'https://feeds.datagolf.com/'

    def __init__(self, **kwargs):
        try:
            self._api_key = open_json_file('secrets.json').get('api_key')
        except FileNotFoundError as e:
            print('Correct secrets.json file')

    def _make_request(self, endpoint, **kwargs):
        """Base function for building a request.
        """
        url = f'{RequestHandler._url_base}{endpoint}?key={self._api_key}&' \
              + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        resp = requests.request("GET", url, headers={}, data={})
        if resp.status_code == 404:
            raise ValueError('Invalid url')  # TODO make exception classes
        if 'file_format=csv' in resp.request.url:
            return [item.split(',') for item in resp.text.split('\n')]
        return json.loads(resp.text)

    def player_list(self, **kwargs):
        """Provides players who've played on a "major tour" since 2018
        or are playing on a major tour this week. IDs, country, amateur status included.
        file_format is json (default), csv
        """
        return self._make_request(endpoint='get-player-list', **kwargs)

    def field_updates(self, **kwargs):
        """Provides field updates on WDs, Monday Qualifiers, tee times.
        tour can be pga (default), euro, kft, opp, alt
        file_format is json (default), csv
        """
        return self._make_request(endpoint='field-updates', **kwargs)

    def tour_schedules(self,  **kwargs):
        """Current season schedules for the primary tours (PGA, European, KFT).
        Includes event names/ids, course names/ids, and location
        (city/country and latitude, longitude coordinates) data for select tours.
        tour (optional) can be pga (default), euro, kft
        """
        return self._make_request(endpoint='get-schedule', **kwargs)
    
    def data_golf_rankings(self, **kwargs):
        """Returns the top 500 players in the current DG rankings, 
           along with each player's skill estimate and respective OWGR rank.
        Args:
            file_format (str, optional): Defaults to 'json'.
        """
        return self._make_request(endpoint='preds/get-dg-rankings', **kwargs)
    
    def pre_tournament_predictions(self, **kwargs):
        """Returns full-field probabilistic forecasts for the upcoming tournament on PGA, European, 
        and Korn Ferry Tours from both our baseline and baseline + course history & fit models. 
        Probabilities provided for various finish positions (make cut, top 20, top 5, win, etc.).

        Args:
           tour (str, optional): pga (default), euro, kft, opp (opposite field PGA TOUR event), alt
           add_position (list[str], optional): 1, 2, 3 .... 48, 49, 50
           odds_format (str, optional): percent (default), american, decimal, fraction
           file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/pre-tournament', **kwargs)

    def get_live_stats(self, **kwargs):
        """Returns live strokes-gained and traditional stats for
        every player during PGA Tour tournaments.
        
        stats (optional): Comma-separated list of statistics to be returned.
            options: sg_putt, sg_arg, sg_app, sg_ott, sg_t2g, sg_bs, sg_total, 
            distance, accuracy, gir, prox_fw, prox_rgh, scrambling

        round (optional) e
            options: event_avg, 1, 2, 3, 4

        display (optional) specifies how stats are displayed
            options: value (default), rank
        
        file_format (optional) 
            options: json (default), csv
        """
        return self._make_request(endpoint='preds/live-tournament-stats', **kwargs)


class CommonHandler:

    def __init__(self, request_handler: RequestHandler):
        self._request_handler = request_handler

    @staticmethod
    def _name_comparison(name: str, target_name: str = '') -> bool:        
        if target_name == '': return False
        is_found = True 
        if target_name:
            for name_part in set(name_part.lower().strip() for name_part in target_name.split()): 
                if name_part not in name.lower(): is_found = False             
        return is_found
    
    def get_players(self, dg_id: int = 0, dg_ids: list[int] = [], 
                       name: str = '', names: list[str] = [], **kwargs) -> list[Player]:
        players = [Player(**player) for player in self._request_handler.player_list(**kwargs)]
        
        if all(not _ for _ in (dg_id, dg_ids, name, names)):
            return players 
        
        target_data: list[Player] = []
        dg_ids = [*dg_ids, dg_id] if dg_id else dg_ids
        names = [*names, name] if name  else names
        for player in players:
            for id_ in dg_ids:
                if id_ == player.dg_id:
                    target_data.append(player)
            for name_ in names:
                if CommonHandler._name_comparison(name=player.player_name, target_name=name_): target_data.append(player)
                        
        return list(OrderedDict.fromkeys(target_data)) if target_data else players
  
    def get_player_field_updates(self, dg_id: int = 0, dg_ids: list[int] = [], 
                                 name: str = '', names: list[str] = [], tour: str = 'pga') -> PlayerFieldUpdates:

        player_field_updates: PlayerFieldUpdates = self._request_handler.field_updates(tour=tour)
        player_field_updates['field'] = [PlayerFieldUpdate(**field_update) for field_update in player_field_updates.get('field')]
        
        if all(not _ for _ in (dg_id, dg_ids, name, names)):
            return player_field_updates
        
        target_data: list[PlayerFieldUpdate] = []
        dg_ids = [*dg_ids, dg_id] if dg_id else dg_ids
        names = [*names, name] if name  else names
        for player_field_update in player_field_updates['field']:
            for dg_id in dg_ids:
                if dg_id == player_field_update.dg_id:
                    target_data.append(player_field_update)
            for name_ in names:
                if CommonHandler._name_comparison(name=player_field_update.player_name, target_name=name_): target_data.append(player_field_update)
        
        player_field_updates['field'] = list(OrderedDict.fromkeys(target_data))         
        return player_field_updates   

    def get_current_tournament(self, **kwargs) -> dict:
        return {k: v for k, v in self._request_handler.field_updates(**kwargs).items() if k == 'event_name'}

    def get_current_round(self, **kwargs) -> dict:
        return {k: v for k, v in self._request_handler.field_updates(**kwargs).items() if k == 'current_round'}
    
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
