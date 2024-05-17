import pytest

from datagolf.api import DgAPI
from datagolf.models import PlayerModel


@pytest.fixture
def api():
    return DgAPI()

@pytest.fixture
def tony_data():
    return [PlayerModel(dg_id=11676, player_name='Finau, Tony', country='United States', country_code='USA', amateur=0)]


@pytest.fixture
def ludvig_spieth_data():
    return set([
        PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE', amateur=0),
        PlayerModel(dg_id=14636, player_name='Spieth, Jordan',country='United States', country_code='USA', amateur=0)
    ])


class TestDgAPI:

    def test_get_players_name(self, api, tony_data):
        assert tony_data == api.get_players( name='tony finau')

    def test_get_players_name_no_spaces(self, api):
        assert api.get_players(name='tonyfinau') == []

    def test_get_player_one_name_one_result(self, api, tony_data):
        assert tony_data == api.get_players(name='finau')

    def test_get_player_one_name_multiple_results(self, api, tony_data):
        test_data = set([
            *tony_data,
            PlayerModel(dg_id=17159, player_name='Omuli, Tony',
                        country='Kenya', country_code='KEN', amateur=0),
            PlayerModel(dg_id=24515, player_name='Romo, Tony',
                        country='United States', country_code='USA', amateur=1),
        ])
        assert test_data == set(api.get_players(name='Tony'))

    def test_get_players_name_all_caps(self, api, tony_data):
        assert tony_data == api.get_players(name='TONY FINAU')

    def test_get_players_names(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == set(api.get_players(name=['ludvig', 'jordan spieth']))

    def test_get_players_id(self, api):
        assert [PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)] == api.get_players(dg_id=23950)

    def test_get_players_id_string(self, api):
        assert [PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)] == api.get_players(dg_id='23950')

    def test_get_players_ids(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == set(api.get_players(dg_id=['23950', 14636]))

    def test_get_players_duplicate_names_in_same_string(self, api, tony_data):
        assert tony_data == api.get_players(name='finau finau')

    def test_get_players_duplicate_ids_list(self, api, tony_data):
        assert tony_data == api.get_players(dg_id=[11676, 11676])

    def test_get_players_multiple_params_with_duplicates(self, api, ludvig_spieth_data, tony_data):
        test_data = set([
            *ludvig_spieth_data,
            *tony_data,
            PlayerModel(dg_id=5321, player_name='Woods, Tiger',
                        country='United States', country_code='USA', amateur=0),
        ])
        assert test_data == set(api.get_players(name=[
                                'ludvig', 'spieth', 'finau'], dg_id=[5321, 23950]))
