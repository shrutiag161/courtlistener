import pytz
from libs import datetime_formatter as dtf
from functools import cached_property

JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Entire Docket (one case)
class Docket:
    def __init__(self, docket_url, token):
        self.docket_url = docket_url
        self.headers = self.__headers(token)
        self.single_docket_json = None
        self.docket_entries_json = None
        self.session = requests.Session()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    
    def _load_docket_json(self, *, api_type):
        if api_type == "single":
            if not self.single_docket_json:
                req_url = self._create_request_url(api_type="single")
                self.single_docket_json = self._response_json(req_url)
        elif api_type == "entries":
            if not self.docket_entries_json:
                req_url = self._create_request_url(api_type="entries")
                self.docket_entries_json = self._response_json(req_url)
        else:
            raise Exception(f"api_type {api_type} is not 'single' or 'entries'")

    def _find_in_json(self, key, *, default=None, json_type):
        if json_type == "single":
            self._load_docket_json(api_type="single")
            return self.single_docket_json.get(key, default)     
        elif json_type == "entries":
            self._load_docket_json(api_type="entries")
            return self.docket_entries_json.get(key, default)           

    def _format_dt_str(self, dt_str):
        central_tz = pytz.timezone('US/Central')
        dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, central_tz)
        new_dt_format = "%A %b %d at %I %p %Z"
        return dtf.format_dt(dt, new_dt_format)

    @property
    def case_name(self):
        return self._find_in_json("case_name", default="Not Found", json_type="single")
    
    @property
    def date_modified(self) -> str:
        date_modified = self._find_in_json("date_modified", json_type="single")
        if date_modified:
            return self._format_dt_str(date_modified)
        return date_modified

    @cached_property
    def entries(self) -> list[dict]:
        all_entries = []
        self._load_docket_json(api_type="entries")
        recent_entries_json = self.docket_entries_json
        all_entries.extend(recent_entries_json["results"])
        next_url = recent_entries_json["next"]
        # while(next_url):
        #     previous_entries_json = self._response_json(next_url)
        #     all_entries.extend(previous_entries_json["results"])
        #     next_url = previous_entries_json["next"]
        return all_entries