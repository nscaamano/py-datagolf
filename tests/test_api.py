import pytest

from datagolf.api import DgAPI

from datagolf.models import PlayerModel


@pytest.fixture
def api():
    return DgAPI()


@pytest.fixture
def player_list(api):
    return api.request.player_list()


@pytest.fixture
def tony_data():
    return PlayerModel(dg_id=11676, player_name='Finau, Tony', country='United States', country_code='USA', amateur=0)


@pytest.fixture
def ludvig_spieth_data():
    return set([
        PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE', amateur=0),
        PlayerModel(dg_id=14636, player_name='Spieth, Jordan',country='United States', country_code='USA', amateur=0)
    ])


class TestDgAPI:

    def test_get_players_name(self, api, player_list, tony_data):
        assert tony_data == api.common.get_players(
            player_list_data=player_list, name='tony finau')

    def test_get_players_name_no_spaces(self, api, player_list):
        assert api.common.get_players(
            player_list_data=player_list, name='tonyfinau') == []

    def test_get_player_one_name_one_result(self, api, player_list, tony_data):
        assert tony_data == api.common.get_players(
            player_list_data=player_list, name='finau')

    def test_get_player_one_name_multiple_results(self, api, player_list, tony_data):
        test_data = set([
            tony_data,
            PlayerModel(dg_id=17159, player_name='Omuli, Tony',
                        country='Kenya', country_code='KEN', amateur=0),
            PlayerModel(dg_id=24515, player_name='Romo, Tony',
                        country='United States', country_code='USA', amateur=1),
        ])
        assert test_data == set(api.common.get_players(
            player_list_data=player_list, name='Tony'))

    def test_get_players_name_all_caps(self, api, player_list, tony_data):
        assert tony_data == api.common.get_players(
            player_list_data=player_list, name='TONY FINAU')

    def test_get_players_names(self, api, player_list, ludvig_spieth_data):
        assert ludvig_spieth_data == set(api.common.get_players(
            player_list_data=player_list, names=['ludvig', 'jordan spieth']))

    def test_get_players_id(self, player_list, api):
        assert PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0) == api.common.get_players(player_list_data=player_list, dg_id=23950)

    def test_get_players_id_string(self, player_list, api):
        assert PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0) == api.common.get_players(player_list_data=player_list, dg_id='23950')

    def test_get_players_ids(self, api, player_list, ludvig_spieth_data):
        assert ludvig_spieth_data == set(api.common.get_players(
            player_list_data=player_list, dg_ids=['23950', 14636]))

    def test_get_players_duplicate_names_in_same_string(self, api, player_list, tony_data):
        assert tony_data == api.common.get_players(
            player_list_data=player_list, name='finau finau')

    def test_get_players_duplicate_ids_list(self, api, player_list, tony_data):
        assert tony_data == api.common.get_players(dg_ids=[11676, 11676])

    def test_get_players_multiple_params_with_duplicates(self, api, player_list, ludvig_spieth_data, tony_data):
        test_data = set([
            *ludvig_spieth_data,
            tony_data,
            PlayerModel(dg_id=5321, player_name='Woods, Tiger',
                        country='United States', country_code='USA', amateur=0),
        ])
        assert test_data == set(api.common.get_players(player_list_data=player_list, name='ludvig', names=[
                                'ludvig', 'spieth'], dg_ids=[5321, 23950], dg_id=11676))
