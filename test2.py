from datagolf.request import RequestHandler

if __name__ == '__main__':
    api = RequestHandler() 

    print(api.get_player_list())
