import requests
from urllib.parse import urlparse

DOCKET_API = "https://www.courtlistener.com/api/rest/v4/dockets/"
ENTRIES_API = "https://www.courtlistener.com/api/rest/v4/docket-entries/?order_by=date_filed&docket="

# connects to the api and returns docket/entries response jsons
class DocketService:
    def __init__(self, token):
        self.__token = token
        self.session = requests.Session()
        self.__headers = {
            'Authorization': f'Token {self.__token}',
        }
    
    """
    Extracts docket id from url
    """
    @staticmethod
    def extract_docket_id(docket_url) -> str:
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
    
    """
    Creates API req url for one docket info
    """
    @staticmethod
    def _create_docket_request_url(docket_id, fields=None):
        request_url = DOCKET_API + docket_id
        if fields:
            fields_str = ",".join(fields)
            request_url = f"{request_url}?fields={fields_str}" 
        return request_url
    
    """
    Creates API req url for a docket's entries (all entries)
    """
    @staticmethod
    def _create_entries_request_url(docket_id):
        return ENTRIES_API + docket_id
    
    """
    Makes get request
    """
    def _get_response(self, url):
        response = self.session.get(url, headers=self.__headers)
        print(f"requested {url}")
        response.raise_for_status() # raises for 4xx or 5xx response
        return response
    
    """
    Gets json response for docket API
    """
    def get_docket_json(self, docket_url:str, *, fields:list[str]=None) -> dict:
        docket_id = DocketService.extract_docket_id(docket_url)
        request_url = DocketService._create_docket_request_url(docket_id, fields)
        response = self._get_response(request_url)
        return response.json()
    
    """
    Iterates through 20 result pagination to get all entries for one docket
    """
    def _get_all_entries(self, entries_json:dict) -> list[dict]:
        all_entries = []
        all_entries.extend(entries_json["results"])
        next_url = entries_json["next"]
        while(next_url):
            next_response = self._get_response(next_url)
            # if next_response.status_code == 429:
            #     print("oopsies rate limited :(((")
            #     time.sleep(5)
            #     continue
            next_entries_json = next_response.json()
            all_entries.extend(next_entries_json["results"])
            next_url = next_entries_json["next"]
        return all_entries

    """
    Calls API and returns all docket entries
    """
    def get_entries(self, docket_url:str) -> list[dict]:
        docket_id = DocketService.extract_docket_id(docket_url)
        request_url = DocketService._create_entries_request_url(docket_id)
        response = self._get_response(request_url)
        entries_page_one_json = response.json()
        return self._get_all_entries(entries_page_one_json)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()