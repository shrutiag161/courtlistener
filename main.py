import requests
from datetime import datetime
import pytz
import logging

DOCKET_URLS = "docket_urls.txt"
TOKEN_FILE_NAME = "token.txt"
API_DOCKET_URL = "https://www.courtlistener.com/api/rest/v4/dockets/"

def read_file_as_list(file_name):
    try:
        with open(file_name) as file:
            content = [line.strip() for line in file if line.strip()] # line.strip() returns true if the line is not empty/not only whitespace
            if not content: # [] is false
                logging.error(f"{file_name} is empty")
            return content
    except FileNotFoundError:
        logging.error(f"No file named {file_name} found")
     
def read_file_as_string(file_name):
    try:
        with open(file_name) as file:
            content = file.read().strip()
            if not content:
                logging.error(f"{file_name} is empty")
            else:
                return content
    except FileNotFoundError:
        logging.error(f"No file named {file_name} found")

def format_datetime(datetime_str):
    format = "%Y-%m-%dT%H:%M:%S.%f%z"
    datetime_dt = datetime.strptime(datetime_str, format) # string to datetime
    eastern_tz = pytz.timezone('US/Eastern')
    datetime_eastern = datetime_dt.astimezone(eastern_tz)
    datetime_formatted = datetime_eastern.strftime("%A %b %d at %I %p %Z") # format datetime
    return datetime_formatted

def get_docket_id(url):
    try:
        url_pieces = url.split('/')
        if("docket" in url_pieces):
            id_index = url_pieces.index("docket")+1
            docket_number = url_pieces[id_index]
            int(docket_number) # make sure the docket id is a number
            return(docket_number)
        else:
            logging.error(f"{url}: the docket url is wrong you dummy")
    except Exception as e:
        logging.error(f"{e}: Couldn't get the docket number from the url")
    
def create_request_url(url):
    docket_id = get_docket_id(url)
    if(docket_id):
        return API_DOCKET_URL + docket_id

token = read_file_as_string(TOKEN_FILE_NAME)
if(not token):
    logging.info("exiting")
    exit(1)

headers = {
    'Authorization': f'Token {token}',
}

docket_urls = read_file_as_list(DOCKET_URLS)
if not docket_urls: 
    exit(1)

for docket_url in docket_urls:
    print("Docket: " + docket_url)
    request_url = create_request_url(docket_url)
    if(not request_url):
        print("\n")
        continue
    response = requests.get(request_url, headers=headers)
    if(response.status_code != 200):
        logging.error(f"Response was {response.status_code}\n")
    else:
        try:
            json = response.json()
            original_datetime = json.get("date_modified")
            readable_datetime = format_datetime(original_datetime)

            print("Case: " + json.get("case_name"))
            print("Latest Update: " + readable_datetime + "\n")
        except Exception as e:
            logging.error(f"{e}: Couldn't parse json response/convert datetime_modified")