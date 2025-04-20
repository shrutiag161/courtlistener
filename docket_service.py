import requests
from functools import cached_property
from urllib.parse import urlparse
import requests

DOCKET_API = "https://www.courtlistener.com/api/rest/v4/dockets/"
ENTRIES_API = "https://www.courtlistener.com/api/rest/v4/docket-entries/?docket="

# connects to the api and returns docket/entries response jsons
class DocketService:
    def __init__(self, token):
        self.__token = token
        self.session = requests.Session()
        self.__headers = {
            'Authorization': f'Token {self.__token}',
        }
    
    @staticmethod
    def _extract_docket_id(docket_url) -> str:
        if not docket_url.startswith("https://www.courtlistener.com/docket/"):
            raise Exception(f"{docket_url} is not a valid courtlistener docket url")
        url = urlparse(docket_url)
        path = url.path.strip('/')        
        path_pieces = path.split('/')
        if len(path_pieces) < 2 or path_pieces[0] != "docket": 
            raise Exception(f"Docket id missing in url dummy: {docket_url}")
        id = path_pieces[1]
        if not id.isdigit():
            raise Exception(f"{id} is not a valid docket id")  
        return id
    
    @staticmethod
    def _create_docket_request_url(docket_id, *, fields=None):
        request_url = DOCKET_API + docket_id
        if fields:
            fields_str = ",".join(fields)
            request_url = f"{request_url}?fields={fields_str}" 
        return request_url
    
    @staticmethod
    def _create_entries_request_url(docket_id):
        return ENTRIES_API + docket_id
    
    def _get_response(self, url):
        response = self.session.get(url, headers=self.__headers)
        print(f"requested {url}")
        response.raise_for_status() # raises for 4xx or 5xx response
        return response
    
    def get_docket_json(self, docket_url:str) -> dict:
        docket_id = self._extract_docket_id(docket_url)
        request_url = self._create_docket_request_url(docket_id)
        response = self._get_response(request_url)
        return response.json()
    
    def _get_all_entries(self, entries_json:dict) -> list[dict]:
        all_entries = []
        all_entries.extend(entries_json["results"])
        next_url = entries_json["next"]
        while(next_url):
            next_entries_json = self._get_response(next_url).json()
            all_entries.extend(next_entries_json["results"])
            next_url = next_entries_json["next"]
        return all_entries

    def get_entries(self, docket_url:str) -> list[dict]:
        if not self._is_valid_docket_url(docket_url):
            raise Exception(f"{docket_url} is not a valid court listener docket url")
        docket_id = self._extract_docket_id(docket_url)
        request_url = self._create_entries_request_url(docket_id)
        response = self._get_response(request_url)
        entries_page_one_json = response.json()
        return self._get_all_entries(entries_page_one_json)