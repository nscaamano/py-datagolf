from datagolf.request import rh
from tabulate import tabulate

def run_tests():
    print(rh.get_player_data(name='Tony Finau finau'))
    print(rh.get_player_data(player_id=18417))
    print(rh.get_player_tee_times(name='scottie scheffler'))
    print(rh.get_player_starting_hole(name='scottie scheffler'))
    print(rh.get_current_tournament())
    print(rh.get_current_round())
    print(rh._get_tour_schedules())
    # print(rh.get_player_field_data(name='tony finau'))

    test = dict(foo='foo')
    test2 = dict(bar='bar')
    print({**test, **test2})

    print(rh._get_live_stats())
    data = rh.get_player_tee_times(names=['jordan spieth', 'cameron young',
                                          'Collin morikawa', 'xander schauffele'])

TEE_TIMES_HEADERS = ['dg_id', 'player_name', 'r1_teetime', 'r2_teetime', 'r3_teetime', 'r4_teetime']
if __name__ == '__main__':


    data = rh.get_player_data(names=['tony finau', 'jordan spieth'], file_format='json')
    #print(data)
    print(tabulate(data))










