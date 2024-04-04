from datagolf.api import DgAPI
from datagolf.models import Player

api = DgAPI() 

def get_player_list_test(): 
    
    player_list = api.request.get_player_list()
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

def get_player_test():
    for player in api.common.get_player_data(names=['jordan']): print(player, '\n' + '-'*14)
    


def run_tests(api):
    #misc_test()
    #get_player_list_test()
    get_player_test()
    


if __name__ == '__main__':

    run_tests(api)