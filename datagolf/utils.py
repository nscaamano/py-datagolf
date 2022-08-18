import os
from pathlib import Path
import json


def open_json_file(filename: str) -> dict:
    with open(os.path.join(Path(os.path.abspath(__file__)).parent.absolute(), filename,)) as f:
        return json.load(f)


def write_json_file(filename: str, data: dict) -> None:
    pass


def convert_json(text: str) -> dict:
    return json.loads(text)

