import pytz
from libs import datetime_formatter as dtf
from functools import cached_property

JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Entire Docket (one case)
class Docket:
    def __init__(self, 
                 docket_id:str,
                 case_name: str,
                 date_modified: str,
                 date_filed: str,
                 assigned_to_str: str,
                 docket_number:str,
                 court_id:str,
                 appeal_from:str):
         self.docket_id = docket_id
         self.case_name = case_name
         self.date_modified = date_modified
         self.date_filed = date_filed
         self.assigned_to_str = assigned_to_str
         self.docket_number = docket_number
         self.court_id = court_id
         self.appeal_from = appeal_from

    @staticmethod
    def _format_dt_str(dt_str):
        central_tz = pytz.timezone('US/Central')
        dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, central_tz)
        new_dt_format = "%A %b %d at %I %p %Z"
        return dtf.format_dt(dt, new_dt_format)
    
    def to_dict(self) -> dict:
        return {
            "docket_id": self.docket_id,
            "case_name": self.case_name, 
            "date_modified": self.date_modified,
            "date_filed": self.date_filed,
            "assigned_to_str": self.assigned_to_str,
            "docket_number": self.docket_number,
            "court_id": self.court_id,
            "appeal_from": self.appeal_from
        }
    
    @classmethod
    def from_json(cls, json:dict) -> "Docket":
        return cls(
            docket_id = json.get("id"),
            case_name = json.get("case_name"),
            date_modified = json.get("date_modified"),
            date_filed = json.get("date_filed"),
            assigned_to_str = json.get("assigned_to_str"),
            docket_number = json.get("docket_number"),
            court_id = json.get("court_id"),
            appeal_from = json.get("appeal_from"),
        )
