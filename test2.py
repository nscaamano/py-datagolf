from datagolf.api import DgAPI
from datagolf.models import Player, Event

api = DgAPI() 

def player_list_test(): 
    
    player_list = api.request.player_list()
    print(player_list)
    
def player_list_test_csv():
    player_list = api.request.player_list(file_format='csv')
    print(player_list)

def misc_test():
    external_data: Player = {'amateur': 0, 'country': 'Sweden', 'country_code': 'SWE', 'dg_id': 23950, 'player_name': 'Aberg, Ludvig'}
    bad_external_data: Player = {'amateur': 0, 'country': 'Sweden', 
                                'country_code': 'SWE', 'dg_id': 'foo bar', 'player_name': 'Aberg, Ludvig',
                                'extra_field': 'foo',
    }
    test_player = Player(**external_data)
    print(test_player.amateur)
    print(test_player.player_name)
    bad_data_test_player = Player(**bad_external_data)
    print(bad_data_test_player)

def players_test():

        
    #player_data = api.common.players(dg_ids=[5321, 11676])
    #player_data = api.common.players(dg_id=23950) # ludvig
    player_data = api.common.players(name='ludvig', names=['ludvig', 'spieth'], dg_ids=[5321, 23950], dg_id=11676)
    for player in player_data:
        print(player)
        print('-' * 14)
    
def test_event_model():
    test_data = {
            "course": "Plantation Course at Kapalua",
            "course_key": "656",
            "event_id": 16,
            "event_name": "The Sentry",
            "latitude": 21.001,
            "location": "Kapalua, HI",
            "longitude": -220.654,
            "start_date": "2024-01-04"
    }
    
    test_event = Event(**test_data)
    print(test_event)
    
def field_updates_test():
    #test = api.request.field_updates(tour='pga')
    #test = api.common.player_field_updates(dg_id=23950)
    #test = api.common.player_field_updates(dg_ids=[23950, 14636])
    #test = api.common.player_field_updates()
    test = api.common.player_field_updates(name='ludvig', names=['ludvig', 'spieth'], dg_id=51856, dg_ids=[51856,14002 ])
    for item in test['field']: 
        print(item)
        print('-'* 14)
        
def test_dg_rankings():
    test = api.request.data_golf_rankings()
    print(test)
    
def test_pre_tournament_predictions():
    
    test = api.request.pre_tournament_predictions()
    print(test)

    


def run_tests():
    #misc_test()
    #player_list_test()
    #players_test()
    #test_event_model()
    #field_updates_test()
    #test_dg_rankings()
    #test_pre_tournament_predictions()
    #player_list_test_csv()
    pass
    


if __name__ == '__main__':
    #print(api.common.current_tournament())
    #print(api.common.current_round())
    #run_tests()
    
    field_updates = api.request.field_updates()
    print(field_updates)
    