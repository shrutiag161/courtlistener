import requests
import pytz
from urllib.parse import urlparse
from libs import datetime_formatter as dtf

SPECIFIC_DOCKET_API = "https://www.courtlistener.com/api/rest/v4/dockets/"
JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

class Docket:
    def __init__(self, docket_url, token):
        self.docket_url = docket_url
        self.headers = self.__headers(token)
        self.json = None
    
    def __headers(self, token):
        return {
            'Authorization': f'Token {token}',
        }

    def __docket_id(self):
        url = urlparse(self.docket_url)
        path = url.path.strip('/')        
        path_pieces = path.split('/')
        if len(path_pieces) < 2 or path_pieces[0] != "docket": 
            raise Exception(f"Docket id missing in url dummy: {self.docket_url}")
        docket_id = path_pieces[1]
        if not docket_id.isdigit(): 
            raise Exception(f"{docket_id} is not a valid docket id")  
        return docket_id
        
    def __specific_docket_request_url(self, fields=None):
        docket_id = self.__docket_id()
        request_url = SPECIFIC_DOCKET_API + docket_id
        if fields:
            fields_str = ",".join(fields)
            return f"{request_url}?fields={fields_str}"
        return request_url

    def __response(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status() # raises for 4xx or 5xx response
        return response

    def __response_json(self, request_url):
        response = self.__response(request_url)
        return response.json()
    
    def __load_json(self):
        if not self.json:
            req_url = self.__specific_docket_request_url()
            self.json = self.__response_json(req_url)

    def __find_in_json(self, key, default=None):
        self.__load_json()
        return self.json.get(key, default)        

    def __format_dt_str(self, dt_str):
        tz = pytz.timezone('US/Central')
        dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, tz)
        new_dt_format = "%A %b %d at %I %p %Z"
        return dtf.format_dt(dt, new_dt_format)

    def case_name(self):
        return self.__find_in_json("case_name", "Not Found")

    def date_modified(self):
        date_modified = self.__find_in_json("date_modified", "Not Found")
        return self.__format_dt_str(date_modified)