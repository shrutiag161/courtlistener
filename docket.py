import pytz
from libs import datetime_formatter as dtf
from functools import cached_property

JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Entire Docket (one case)
class Docket:
    def __init__(self, json:dict):
        self.json = json

    def _find_in_json(self, key, *, default=None):
        return self.json.get(key, default)           

    # def _format_dt_str(self, dt_str):
    #     central_tz = pytz.timezone('US/Central')
    #     dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, central_tz)
    #     new_dt_format = "%A %b %d at %I %p %Z"
    #     return dtf.format_dt(dt, new_dt_format)

    @property
    def case_name(self):
        return self._find_in_json("case_name", default="Not Found")
    
    @property
    def date_modified(self) -> str:
        date_modified = self._find_in_json("date_modified")
        # if date_modified:
        #     return self._format_dt_str(date_modified)
        return date_modified