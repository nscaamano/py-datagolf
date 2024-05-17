import os
from pathlib import Path
import json
import csv
from typing import List


def open_json_file(filename: str) -> dict:
    with open(os.path.join(Path(os.path.abspath(__file__)).parent.absolute(), filename,)) as f:
        return json.load(f)


def write_json_file(filename: str, data: dict) -> None:
    pass


def write_dict_data_to_csv(filename: str, data: List[dict]) -> None: 
    with open(os.path.join(Path(os.path.abspath(__file__)).parent.parent.absolute(), filename,), 'w', newline='') as csvfile:
        field_names = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def name_comparison(name: str, target_name: str = '') -> bool:        
        if target_name == '': return False
        is_found = True 
        if target_name:
            for name_part in set(name_part.lower().strip() for name_part in target_name.split()): 
                if name_part not in name.lower(): is_found = False             
        return is_found
