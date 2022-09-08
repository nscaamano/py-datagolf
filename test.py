from datagolf.request import gh
from tabulate import tabulate

from datagolf.golf_models import Player


def run_tests():
    print(gh.get_player_data(name='Tony Finau finau'))
    print(gh.get_player_data(player_id=18417))
    print(gh.get_player_tee_times(name='scottie scheffler'))
    print(gh.get_player_starting_hole(name='scottie scheffler'))
    print(gh.get_current_tournament())
    print(gh.get_current_round())
    print(gh._request_handler.get_tour_schedules())
    # print(rh.get_player_field_data(name='tony finau'))

    test = dict(foo='foo')
    test2 = dict(bar='bar')
    print({**test, **test2})

    print(gh._request_handler.get_live_stats())
    data = gh.get_player_tee_times(names=['jordan spieth', 'cameron young',
                                          'Collin morikawa', 'xander schauffele'])


    # data = rh.get_player_data(names=['tony finau', 'jordan spieth'], file_format='json')
    # show_data(data)

def get_player_data_test():
    # names = ['jordan spieth', 'cameron young', 'Collin morikawa', 'xander schauffele']
    names = ['CAMERON']
    data = gh.get_player_data(names=names)
    for player in data:
        print(player)

def show_data(data):
    print(tabulate(data))

TEE_TIMES_HEADERS = ['dg_id', 'player_name', 'r1_teetime', 'r2_teetime', 'r3_teetime', 'r4_teetime']
if __name__ == '__main__':

    #models_test()
    get_player_data_test()















