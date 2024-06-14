import datetime
import pytest

from datagolf.api import DgAPI
from datagolf.models import (
    PlayerModel, 
    TourSchedulesModel, 
    EventModel,
    PlayerFieldUpdatesModel,
    LiveHoleScoringDistributions
)


@pytest.fixture
def api():
    return DgAPI()

@pytest.fixture
def tony_data():
    return {PlayerModel(dg_id=11676, player_name='Finau, Tony', country='United States', country_code='USA', amateur=0)}


@pytest.fixture
def ludvig_spieth_data():
    return {
        PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE', amateur=0),
        PlayerModel(dg_id=14636, player_name='Spieth, Jordan',country='United States', country_code='USA', amateur=0)
    }


class TestDgAPI:

    def test_get_players_name(self, api, tony_data):
        assert tony_data == api.get_players(player_name='tony finau')

    def test_get_players_name_no_spaces(self, api):
        assert api.get_players(player_name='tonyfinau') == set()

    def test_get_player_one_name_one_result(self, api, tony_data):
        assert tony_data == api.get_players(player_name='finau')

    def test_get_player_one_name_multiple_results(self, api, tony_data):
        test_data = {
            *tony_data,
            PlayerModel(dg_id=17159, player_name='Omuli, Tony',
                        country='Kenya', country_code='KEN', amateur=0),
            PlayerModel(dg_id=24515, player_name='Romo, Tony',
                        country='United States', country_code='USA', amateur=1),
        }
        assert test_data == api.get_players(player_name='Tony')

    def test_get_players_name_all_caps(self, api, tony_data):
        assert tony_data == api.get_players(player_name='TONY FINAU')

    def test_get_players_names(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == api.get_players(player_name=['ludvig', 'jordan spieth'])

    def test_get_players_id(self, api):
        assert {PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)} == api.get_players(dg_id=23950)

    def test_get_players_id_string(self, api):
        assert {PlayerModel(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)} == api.get_players(dg_id='23950')

    def test_get_players_ids(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == api.get_players(dg_id=['23950', 14636])

    def test_get_players_duplicate_names_in_same_string(self, api, tony_data):
        assert tony_data == api.get_players(player_name='finau finau')

    def test_get_players_duplicate_ids_list(self, api, tony_data):
        assert tony_data == api.get_players(dg_id=[11676, 11676])

    def test_get_players_multiple_params_with_duplicates(self, api, ludvig_spieth_data, tony_data):
        test_data = {
            *ludvig_spieth_data,
            *tony_data,
            PlayerModel(dg_id=5321, player_name='Woods, Tiger',
                        country='United States', country_code='USA', amateur=0),
        }
        assert test_data == api.get_players(player_name=[
                                'ludvig', 'spieth', 'finau'], dg_id=[5321, 23950])

    def test_get_tour_schedules_list_event_ids(self, api):
        test_data = TourSchedulesModel(
            current_season=2024,
            schedule={
                EventModel(event_id='28', event_name='Miami', course_key='21', location='Miami, FL', course='Trump National Doral', latitude=25.813, longitude=-80.339, start_date=datetime.date(2024, 4, 5), tour='alt (liv golf)'), 
                EventModel(event_id=14, event_name='Masters Tournament', course_key='014', location='Augusta, GA', course='Augusta National Golf Club', latitude=33.5, longitude=-82.02, start_date=datetime.date(2024, 4, 11), tour='pga'), 
                EventModel(event_id=28, event_name='BMW Championship', course_key='406', location='Castle Rock, CO', course='Castle Pines Golf Club', latitude=39.441, longitude=-104.899, start_date=datetime.date(2024, 8, 22), tour='pga'),    
            },
            tour='alt (liv golf), pga, kft, euro'
        )   
        
        assert test_data == api.get_tour_schedules(event_id=[14, 28])
        
    def test_get_tour_schedules_event_id_and_tour(self, api):
        test_data = TourSchedulesModel(
            current_season=2024,
            schedule={
                EventModel(event_id=14, event_name='Masters Tournament', course_key='014', 
                           location='Augusta, GA', course='Augusta National Golf Club', 
                           latitude=33.5, longitude=-82.02, start_date=datetime.date(2024, 4, 11), tour=None
                )
            },
            tour='pga'
        )
        
        assert test_data == api.get_tour_schedules(event_name='masters', tour='pga')
    
    def test_get_player_field_updates(self, api):
        assert isinstance(api.get_player_field_updates(), PlayerFieldUpdatesModel)
        
    def test_get_player_field_updates_str_filter_field(self, api):
        assert isinstance(api.get_player_field_updates(country='USA'), PlayerFieldUpdatesModel)
    
    def test_live_hole_scoring_distributions(self, api):
        assert isinstance(api.get_live_hole_scoring_distributions(), LiveHoleScoringDistributions)