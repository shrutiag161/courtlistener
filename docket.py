import requests
import pytz
from urllib.parse import urlparse

from libs import file_reader as fr
from libs import datetime_formatter as dtf

SPECIFIC_DOCKET_API = "https://www.courtlistener.com/api/rest/v4/dockets/"
JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
BASE_DOCKET_URL = "https://www.courtlistener.com/"

class DocketRequest:
    def __init__(self, docket_url, token):
        self.docket_url = docket_url
        self.headers = self._headers(token)
        self.json = None
    
    @staticmethod
    def _headers(token):
        return {
            'Authorization': f'Token {token}',
        }

    def _docket_id(self):
        path = self.docket_url.strip(BASE_DOCKET_URL)  # Removes the base part directly from the URL
        path_pieces = path.split('/')
        # ??? check!
        if len(path_pieces) < 1 or path_pieces[0] != "docket": 
            raise Exception(f"Docket id missing in url dummy: {self.docket_url}")
        docket_id = path_pieces[1]
        if not docket_id.isdigit(): # make sure the docket id is a number
            raise Exception(f"{docket_id} is not a valid docket id")  
        return docket_id
        
    def _specific_docket_request_url(self, fields=None):
        docket_id = self._docket_id()
        request_url = SPECIFIC_DOCKET_API + docket_id
        if(fields):
            fields_str = ",".join(fields)
            return f"{request_url}?fields={fields_str}"
        return request_url

    def response(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status() # raises for 4xx or 5xx response
        return response

    def response_json(self, request_url):
        response = self.response(request_url)
        return response.json()
    
    def format_dt_str(self, dt_str):
        eastern_tz = pytz.timezone('US/Eastern')
        new_dt_format = "%A %b %d at %I %p %Z"
        dt_str_formatted = dtf.format_datetime(dt_str, JSON_RESPONSE_DATETIME_FORMAT, eastern_tz, new_dt_format)
        return dt_str_formatted

    def load_json(self):
        if(not self.json):
            req_url = self._specific_docket_request_url()
            self.json = self.response_json(req_url)

    def case_name(self):
        self.load_json()
        return self.json.get("case_name", "Not Found")


    def date_modified(self):
        self.load_json()
        date_modified = self.json.get("date_modified", "Not Found")
        return self.format_dt_str(date_modified)
        
    
    