from functools import cached_property

# One single docket entry
class DocketEntry:
    FIELDS_TO_EXPORT = ["id",
                        "date_filed", 
                        "date_modified",
                        "entry_number",
                        "description"]
    def __init__(self, json:dict, docket_id:str):
        self.json = json
        self.docket_id = docket_id    

    @staticmethod
    def _update_entry_id(entry: dict) -> dict:
        entry["entry_id"] = entry.pop("id")
        return entry
    
    @staticmethod
    def _add_docket_id(self, entry: dict, docket_id:str) -> dict:
        entry["docket_id"] = self.docket_id
        return entry

    def to_dict(self):
        output = {}
        for field in self.FIELDS_TO_EXPORT:
            if hasattr(self, field):
                output[field] = getattr(self, field)
            else:
                output[field] = self.json.get(field)
        output = self._update_entry_id(output)
        output = self._add_docket_id(output, self.docket_id)
        return output
