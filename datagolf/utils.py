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
