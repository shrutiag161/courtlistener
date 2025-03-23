import requests
import pytz
import logging
import sys

from libs import file_reader as fr
from libs import datetime_formatter as dtf

API_DOCKET_URL = "https://www.courtlistener.com/api/rest/v4/dockets/"
JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
BASE_DOCKET_URL = "https://www.courtlistener.com/docket/"
TOKEN_FILE = "token.txt"

token = fr.read_file_as_string(TOKEN_FILE)
if not token:
    sys.exit(f"{TOKEN_FILE} is empty")

headers = {
    'Authorization': f'Token {token}',
}

def get_docket_id(docket_url):
    if not docket_url.startswith(BASE_DOCKET_URL):
            raise Exception(f"The docket url is wrong dummy: {docket_url}")
    rest_of_url = docket_url[len(BASE_DOCKET_URL):]
    if len(rest_of_url) < 1: # there should be a docket id after the base docket url
        raise Exception(f"Docket id missing in url")
    url_pieces = rest_of_url.split('/')
    docket_id = url_pieces[0]
    if docket_id.isdigit(): # make sure the docket id is a number
        return docket_id
    else:
        raise Exception(f"{docket_id} is not a valid docket id")  
    
def create_docket_request_url(docket_url):
    docket_id = get_docket_id(docket_url)
    return API_DOCKET_URL + docket_id

def get_response(url, headers):
    return requests.get(url, headers=headers)

def get_docket_json(docket_url):
    request_url = create_docket_request_url(docket_url)
    response = get_response(request_url, headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}\n")
    json = response.json()
    return json
    
def get_last_updated_timestamp(json):
    json_dt_field = "date_modified"
    last_update_dt = json.get(json_dt_field)
    if(last_update_dt):
        eastern_tz = pytz.timezone('US/Eastern')
        new_dt_format = "%A %b %d at %I %p %Z"
        last_update_dt_formatted = dtf.format_datetime(last_update_dt, JSON_RESPONSE_DATETIME_FORMAT, eastern_tz, new_dt_format)
        return last_update_dt_formatted
    else:
        return "Not found"
    
def get_case_name(json):
    return json.get("case_name", "Not found")