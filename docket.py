import requests
import pytz
from urllib.parse import urlparse
from libs import datetime_formatter as dtf

single_DOCKET_API = "https://www.courtlistener.com/api/rest/v4/dockets/"
entries_DOCKET_API = "https://www.courtlistener.com/api/rest/v4/docket-entries/?docket="
JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

class Docket:
    def __init__(self, docket_url, token):
        self.docket_url = docket_url
        self.headers = self.__headers(token)
        self.docket_id = None
        self.single_docket_json = None
        self.docket_entries_json = None
    
    def __headers(self, token):
        return {
            'Authorization': f'Token {token}',
        }

    def _docket_id(self):
        if not self.docket_id:
            url = urlparse(self.docket_url)
            path = url.path.strip('/')        
            path_pieces = path.split('/')
            if len(path_pieces) < 2 or path_pieces[0] != "docket": 
                raise Exception(f"Docket id missing in url dummy: {self.docket_url}")
            docket_id = path_pieces[1]
            if not docket_id.isdigit(): 
                raise Exception(f"{docket_id} is not a valid docket id")  
            self.docket_id = docket_id
        return self.docket_id
        
    def _create_request_url(self, *, api_type, fields=None):
        docket_id = self._docket_id()
        if api_type=="single":
            request_url = single_DOCKET_API + docket_id
            if fields:
                fields_str = ",".join(fields)
                request_url = f"{request_url}?fields={fields_str}" 
        elif api_type == "entries":
            request_url = entries_DOCKET_API + docket_id
        return request_url

    def _response(self, url):
        print(f"making request {url}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status() # raises for 4xx or 5xx response
        return response

    def _response_json(self, request_url):
        response = self._response(request_url)
        return response.json()
    
    def _load_docket_json(self, *, api_type):
        if api_type == "single":
            if not self.single_docket_json:
                req_url = self._create_request_url(api_type="single")
                self.single_docket_json = self._response_json(req_url)
        elif api_type == "entries":
            if not self.docket_entries_json:
                req_url = self._create_request_url(api_type="entries")
                self.docket_entries_json = self._response_json(req_url)

    def _find_in_json(self, key, *, default=None, json_type):
        if json_type == "single":
            self._load_docket_json(api_type="single")
            return self.single_docket_json.get(key, default)     
        elif json_type == "entries":
            self._load_docket_json(api_type="entries")
            return self.docket_entries_json.get(key, default)           

    def _format_dt_str(self, dt_str):
        tz = pytz.timezone('US/Central')
        dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, tz)
        new_dt_format = "%A %b %d at %I %p %Z"
        return dtf.format_dt(dt, new_dt_format)

    def case_name(self):
        return self._find_in_json("case_name", default="Not Found", json_type="single")

    def date_modified(self):
        date_modified = self._find_in_json("date_modified", default="Not Found", json_type="single")
        return self._format_dt_str(date_modified)
    
    # def count(self):
    #     count_url = self._find_in_json("count", json_type="entries")
    #     count_json = self._response_json(count_url)
    #     return count_json["count"]
    
    # def pages(self):
    #     count = self.count()
    #     return count/20
    
    def id(self):
        return self._docket_id()
    
    def entries(self):
        all_entries = []
        self._load_docket_json(api_type="entries")
        recent_entries_json = self.docket_entries_json
        all_entries.extend(recent_entries_json["results"])
        next_url = recent_entries_json["next"]
        while(next_url):
            previous_entries_json = self._response_json(next_url)
            all_entries.extend(previous_entries_json["results"])
            next_url = previous_entries_json["next"]
        return all_entries