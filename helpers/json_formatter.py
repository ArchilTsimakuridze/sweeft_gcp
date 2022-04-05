import json


def json_to_dict(file_path):
    """Returns a dictionary of a given JSON """
    with open(file_path) as json_file:
        return json.load(json_file)
