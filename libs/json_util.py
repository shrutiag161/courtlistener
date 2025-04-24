def rename_field(json:dict, old_name, new_name):
    if old_name in json:
        json[new_name] = json.pop(old_name)
    return json

def simplify_json(json:dict, fields_to_keep:list[str]) -> dict:
    new_json = {}
    for field in fields_to_keep:
        if field in json:
            new_json[field] = json.get(field)
    return new_json

def add_field(json:dict, field_name, value) -> dict:
    json[field_name] = value
    return json
