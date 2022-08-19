import json
import requests

from .utils import open_json_file


class RequestHandler:
    """Handler for requests against the datagolf API.
    """

    _url_base = 'https://feeds.datagolf.com/'

    def __init__(self, **kwargs):
        try:
            self._api_key = open_json_file('secrets.json').get('api_key')
        except FileNotFoundError as e:
            print('Correct secrets.json file')

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

    def _get_player_list(self, file_format='json'):
        """Provides players who've played on a "major tour" since 2018
        or are playing on a major tour this week. IDs, country, amateur status included.
        file_format is json (default), csv
        """
        return self._make_request(action='get-player-list', **{'file_format': file_format})

    def _get_field_updates(self, tour='pga', file_format='json'):
        """Provides field updates on WDs, Monday Qualifiers, tee times.
        tour can be pga (default), euro, kft, opp, alt
        file_format is json (default), csv
        """
        return self._make_request(action='field-updates', **{'tour': tour, 'file_format': file_format})

    def _get_tour_schedules(self,  tour='pga', file_format='json'):
        return self._make_request(action='get-schedule', **{'tour': tour, 'file_format': file_format})

    def _get_live_stats(self, **kwargs):
        """Returns live strokes-gained and traditional stats for
        every player during PGA Tour tournaments.
        """
        return self._make_request(action='preds/live-tournament-stats', **kwargs)

    @staticmethod
    def _is_player(player_object: dict, target_name,
                   target_player_id: int) -> bool:
        """Player data comparisons.
        TODO use dataclass for comparisons? Models for this player object stuff
              account for one name only or longer name i.e. 3 names; possible?
              len(target_name) > 1 is bad
        """
        if target_player_id:
            return True if player_object.get('dg_id') == int(target_player_id) else False
        else:
            if target_name and len(target_name) > 1:
                name = set([name.lower().strip() for name in player_object.get('player_name').split(',')])
            else:
                raise ValueError('Invalid Name Format')  # TODO make own exceptions classes
            return True if target_name == name else False

    def get_player_data(self, name=None, player_id=None) -> dict:
        for player_object in self._get_player_list():
            if self._is_player(player_object,
                               set([name.lower().strip() for name in name.split()]) if name else None, player_id):
                return player_object

    def get_player_field_data(self, name=None, player_id=None) -> dict:
        for player_object in self._get_field_updates().get('field'):
            if self._is_player(player_object,
                               set([name.lower().strip() for name in name.split()]) if name else None, player_id):
                return player_object   # DATACLASS????

    def get_player_tee_times(self, name=None, player_id=None) -> dict:
        return {k: v for k, v in self.get_player_field_data(name, player_id).items()
                if 'teetime' in k or k in ['dg_id', 'player_name']}

    def get_player_tee_times(self, **kwargs) -> list:
        return [{k: v for k, v in self.get_player_field_data(name=name).items()
                if 'teetime' in k or k in ['dg_id', 'player_name']} for name in kwargs.get('names')]


    def get_player_starting_hole(self, name=None, player_id=None):
        return {k: v for k, v in self.get_player_field_data(name, player_id).items()
                if k in ['dg_id', 'player_name', 'start_hole']}

    def get_current_tournament(self, **kwargs) -> str:
        return self._get_field_updates(**kwargs).get('event_name')

    def get_current_round(self, **kwargs):
        return self._get_field_updates(**kwargs).get('current_round')

rh = RequestHandler()


