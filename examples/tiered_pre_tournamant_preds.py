from datagolf.api import Api
#from lookups.pga_champ_2024 import TIERS
from lookups.us_open_2024 import TIERS
from datagolf.models import PreTournamentPredModel
from datagolf.utils import write_dict_data_to_csv

#  note add to env
#  export PYTHONPATH=/path/to/py-datagolf


PRED_MODEL = 'baseline_history_fit'
TOURNAMENT_PREFIX = 'usopen'


if __name__ == '__main__':
    api = Api()
    
    preds = api._request.pre_tournament_predictions()  # TODO replace with api once supported
    output = {}
    
    for tier, values in TIERS.items():
        dg_ids = [player.dg_id for player in api.get_players(player_name=values)]
        output_preds = []
        for pred in preds[PRED_MODEL]:  # once supported by api use . notation
            if pred['dg_id'] in dg_ids:
                output_preds.append(pred)
        output[tier] = output_preds
        
    for tier, data in output.items():
        write_dict_data_to_csv(filename=f'examples/output/pre_tournament_preds_{TOURNAMENT_PREFIX}_{tier.lower()}.csv', data=data)

        
