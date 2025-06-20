from datagolf.api import DgAPI
from datagolf.request import RequestHandler

if __name__ == '__main__':
    api = DgAPI()
    #print(api.get_tour_schedules(event_name='masters', tour='pga'))
    rh = RequestHandler()
    
    field_updates = rh.field_updates()
    print(sorted(list(field_updates.keys())))