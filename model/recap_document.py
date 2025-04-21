# One single recap document - document attached to entry
class RecapDocument:
    def __init__(self, recap_doc_json:dict):
        self.json = recap_doc_json

    def _find_in_json(self, key, *, default=None):
        return self.json.get(key, default)           