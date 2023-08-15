import json


def load_json(file_name):
    try:
        with open(file_name) as file:
            return json.load(file)
    except:
        return None


def save_json(src_dict: dict, target_file: str):
    try:
        with open(target_file, "w") as file:
            json.dump(src_dict, file)
        return True
    except:
        return False


