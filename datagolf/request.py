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

    def get_player_data(self, first_name=None, last_name=None, player_id=None):
        # TODO binary search here at some point
        # TODO support for just first name or last and if conflicts present
        #      message use full name and present ids as alternative
        #      If two players have same full name then use ID.
        # TODO generally this function needs work

        for player in self._get_player_list():
            names = [name.lower().strip() for name in player.get('player_name').split(',')]
            id_ = player.get('dg_id')

            if first_name.lower() in names and last_name.lower() in names:
                return player

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


rh = RequestHandler()


