import requests

from .utils import open_json_file, convert_json


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
        return convert_json(requests.request("GET", url, headers={}, data={}).text)

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

    def _get_tour_schedules(self, file_format='json', tour='pga'):
        return self._make_request(action='get-schedule', **{'tour': tour, 'file_format': file_format})

    @staticmethod
    def _is_player(player_object: dict, target_name,
                   target_player_id: int) -> bool:
        """Player data comparisons.
        TODO use dataclass for comparisons? Models for this player object stuff
              account for one name only or longer name i.e. 3 names; possible?
              len(target_name) > 1 is bad
        """
        if target_player_id and player_object.get('dg_id') == int(target_player_id):
            return True
        if len(target_name) > 1:
            name = set([name.lower().strip() for name in player_object.get('player_name').split(',')])
        else:
            raise ValueError('Invalid Name Format')  # TODO make own exceptions classes
        return True if target_name == name else False

    def get_player_data(self, name=None, player_id=None):
        for player_object in self._get_player_list():
            if self._is_player(player_object, set([name.lower().strip() for name in name.split()]), player_id):
                return player_object

    def get_player_tee_times(self, name=None, player_id=None):
        for player_object in self._get_field_updates().get('field'):
            if self._is_player(player_object, set([name.lower().strip() for name in name.split()]), player_id):
                return {k: v for k, v in player_object.items() if 'teetime' in k
                        or k in ['dg_id', 'player_name']}

    def get_current_tournament(self):
        pass

    def get_current_round(self):
        pass

    def get_field_data(self):
        pass

    def get_starting_hole(self):
        pass

    def tee_times(self):
        pass

    def get_live_stats(self):
        pass

    def get_favorite_players(self):
        pass

    def is_playing(self):
        # is the player playing -> bool
        pass

rh = RequestHandler()


