import requests
from .utils import open_json_file, convert_json

import json

# TODO
#   add meta data for potential items
#   remove defaults from function def
#   implement local cache. Check if anything has updated before grabbing stuff from api
#    have local favorite players to get quick results for players of interest
#    maybe use dataclass for player object for comparison down the line
#    May need to split up request logic into separate structs.
#       for example, FieldUpdatesHandler
#        or may need to use data models


class RequestHandler:

    url_base = 'https://feeds.datagolf.com/'

    def __init__(self, **kwargs):
        try:
            self._api_key = open_json_file('secrets.json').get('api_key')
        except FileNotFoundError as e:
            print('Correct secrets.json file')

    def _make_request(self, action, **kwargs):

        url = f'{RequestHandler.url_base}{action}?key={self._api_key}&' \
         + '&'.join([f'{k}={v}' for k, v in kwargs.items()])

        return convert_json(requests.request("GET", url, headers={}, data={}).text)

    def _get_field_updates(self, tour='pga', file_format='json'):
        """
        :param tour: pga (default), euro, kft, opp, alt
        :param file_format: json (default), csv
        """
        return self._make_request(action='field-updates', **{'tour': tour, 'file_format': file_format})

    def _get_player_list(self, file_format='json'):
        """
        :param file_format: json (default), csv
        :return:
        """
        return self._make_request(action='get-player-list', **{'file_format': file_format})

    def _get_tour_schedules(self, file_format='json', tour='pga'):
        """

        :param file_format: json (default), csv
        :param tour: pga (default), euro, kft
        :return:
        """
        return self._make_request(action='get-schedule', **{'tour': tour, 'file_format': file_format})

    @staticmethod
    def _is_player(player_object: dict, target_first_name: str, target_last_name: str,
                   target_player_id: int) -> bool:

        if target_player_id and player_object.get('dg_id') == int(target_player_id):
            return True

        if target_first_name and target_last_name:
            names = [name.lower().strip() for name in player_object.get('player_name').split(',')]

            if target_first_name.lower() in names and target_last_name.lower() in names:
                return True
        return False

    def get_player_data(self, first_name=None, last_name=None, player_id=None):
        # TODO binary search here at some point
        # TODO support for just first name or last and if conflicts present
        #      tell user to use full name and present ids as alternative
        #      If two players have same full name then use ID.

        for player_object in self._get_player_list():
            if self._is_player(player_object, first_name, last_name, player_id):
                return player_object

    def get_player_tee_times(self, first_name=None, last_name=None, player_id=None):
        for player_object in self._get_field_updates().get('field'):
            if self._is_player(player_object, first_name, last_name, player_id):
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


