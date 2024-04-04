import json
import requests
from collections import OrderedDict

from .utils import open_json_file
from .models import Player

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

    # TODO default value for action ?
    def _make_request(self, action, **kwargs):
        """Base function for building a request.
        API appears to only provide endpoints for GET methods.
        Payloads are delivered via querystring.
        """
        url = f'{RequestHandler._url_base}{action}?key={self._api_key}&' \
              + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        resp = requests.request("GET", url, headers={}, data={})
        if resp.status_code == 404:
            raise ValueError('Invalid url')  # TODO make exception classes
        if 'file_format=csv' in resp.request.url:
            return [item.split(',') for item in resp.text.split('\n')]
        return json.loads(resp.text)

    def get_player_list(self, **kwargs):
        """Provides players who've played on a "major tour" since 2018
        or are playing on a major tour this week. IDs, country, amateur status included.
        file_format is json (default), csv
        """
        return self._make_request(action='get-player-list', **kwargs)

    def get_field_updates(self, **kwargs):
        """Provides field updates on WDs, Monday Qualifiers, tee times.
        tour can be pga (default), euro, kft, opp, alt
        file_format is json (default), csv
        """
        return self._make_request(action='field-updates', **kwargs)

    def get_tour_schedules(self,  **kwargs):
        """Current season schedules for the primary tours (PGA, European, KFT).
        Includes event names/ids, course names/ids, and location
        (city/country and latitude, longitude coordinates) data for select tours.
        tour (optional) can be pga (default), euro, kft
        """
        return self._make_request(action='get-schedule', **kwargs)

    def get_live_stats(self, **kwargs):
        """Returns live strokes-gained and traditional stats for
        every player during PGA Tour tournaments.
        stats optional
        stats (optional) can be list of sg_putt, sg_arg, sg_app, sg_ott, sg_t2g,
        sg_total, distance, accuracy, gir, prox_fw, prox_rgh, scrambling.

        round (optional) event_avg, 1, 2, 3, 4

        display (optional) specifies how stats are displayed and
        can be  value (default), rank
        """
        return self._make_request(action='preds/live-tournament-stats', **kwargs)


class CommonHandler:

    def __init__(self, request_handler: RequestHandler):
        self._request_handler = request_handler

    @staticmethod
    def _is_player(player: Player, target_player_name: str = None, target_player_id: int = None) -> bool:
        # TODO support for ids 
        # could probably combine ids and names into same list and iterate over.
        # check name and id simultaneously 
        
        # for now cannot have both populatated
        #assert not target_player_id and not target_player_name
        if target_player_name and target_player_id: raise Exception('Both id and name cannot be populated at the same time.')
        
        is_found = True 
        if target_player_name:
            for name_part in set(name_part.lower().strip() for name_part in target_player_name.split()): 
                if name_part not in player.player_name.lower(): is_found = False 
                
        if target_player_id and not int(target_player_id) == player.dg_id: is_found = False
            
        return is_found
        
    def get_player_data(self, player_name: str = None, player_id: int = None, 
                        player_names: list[str] = None, player_ids: list[int] = None, 
                        **kwargs) -> list[Player]:
        target_players = []
        for player in self._request_handler.get_player_list(**kwargs):
            player = Player(**player) # could throw exception 
            if player_names: # might not even need this if check because if no true then no append 
                for name in player_names: 
                    if CommonHandler._is_player(player=player, target_player_name=name): target_players.append(player)
                    #name = tuple(name_.lower().strip() for name_ in name.split())
                    #if self._is_player(player=player, target_name=name): player_data.append(Player(**player))
            if player_ids:
                for id_ in player_ids:
                    if CommonHandler._is_player(player=player, target_player_id=id_): target_players.append(player)
            if player_name and CommonHandler._is_player(player=player, target_player_name=player_name): target_players.append(player)
            if player_id and CommonHandler._is_player(player=player, target_player_id=player_id): target_players.append(player)
        return list(OrderedDict.fromkeys(target_players))

    def _general_filtered_get(self, request_func, exception_field, names: list, **kwargs):
        player_ids = [player.dg_id for player in self.get_player_data(names=names)]
        data = request_func(**kwargs)
        if _ERROR in data.keys():
            return data.get(_ERROR)
        output_data = {k: v for k, v in data.items() if k != exception_field}
        for object_ in data.get(exception_field):
            if object_['dg_id'] in player_ids:
                output_data[object_['player_name']] = object_
        return output_data

    def get_player_field_data(self, names: list, **kwargs) -> dict:
        return self._general_filtered_get(request_func=self._request_handler.get_field_updates,
                                          exception_field='field',
                                          names=names, **kwargs)

    def get_current_tournament(self, **kwargs) -> dict:
        return {k: v for k, v in self._request_handler.get_field_updates(**kwargs).items() if k == 'event_name'}

    def get_current_round(self, **kwargs) -> dict:
        return {k: v for k, v in self._request_handler.get_field_updates(**kwargs).items() if k == 'current_round'}

    def get_player_live_stats(self, names: list, **kwargs) -> dict:
        """stats should be a string comma separated list
           i.e. stats='sg_putt,sg_app'
        """
        if 'stats' in kwargs.keys():
            assert ' ' not in kwargs['stats'], "stats should not have spaces. i.e. stats='sg_putt,sg_app'"
        return self._general_filtered_get(request_func=self._request_handler.get_live_stats,
                                          exception_field='live_stats',
                                          names=names, **kwargs)
