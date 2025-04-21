from functools import cached_property

# One single docket entry
class DocketEntry:
    def __init__(self, json:dict):
        self.json = json

    def _find_in_json(self, key, *, default=None):
        return self.json.get(key, default)           