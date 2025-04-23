import pytz
from libs import datetime_formatter as dtf
from functools import cached_property

JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Entire Docket (one case)
class Docket:
    FIELDS_TO_EXPORT = [
        "id",
        "case_name",
        "date_modified",
        "date_filed",
        "assigned_to_str",
        "docket_number",
        "court_id",
        "appeal_from"
    ]
    def __init__(self, json:dict):
        self.json = json
        self.id = json.get("id")

    @staticmethod
    def _format_dt_str(dt_str):
        central_tz = pytz.timezone('US/Central')
        dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, central_tz)
        new_dt_format = "%A %b %d at %I %p %Z"
        return dtf.format_dt(dt, new_dt_format)
    
    @property
    def date_modified(self):
        date_modified = self.json.get("date_modified")
        return Docket._format_dt_str(date_modified) if date_modified else None
    
    def to_dict(self):
        output = {}
        for field in self.FIELDS_TO_EXPORT:
            if hasattr(self, field):
                output[field] = getattr(self, field)
            else:
                output[field] = self.json.get(field)
        return output