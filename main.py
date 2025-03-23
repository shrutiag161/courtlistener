import docket as dr
from libs import file_reader as fr
import logging
import sys

# https://www.courtlistener.com/docket/69746454/20/state-of-maryland-v-usda/

DOCKET_URLS_FILE = "docket_urls.txt"
TOKEN_FILE = "token.txt"

docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True) 
if not docket_urls: 
    logging.error(f"{DOCKET_URLS_FILE} is empty")
    sys.exit(1)

def get_token():
    token = fr.read_file_as_string(TOKEN_FILE)
    if not token:
        logging.error(f"{TOKEN_FILE} is empty")
        sys.exit(1)
    return token

token = get_token()

for docket_url in docket_urls:
    print(f"Docket: {docket_url}")
    try:
        docket_req = dr.DocketRequest(docket_url, token)
        print(f"Case: {docket_req.case_name()}")
        print(f"Last Updated: {docket_req.date_modified()}\n")
    except Exception as e:
        logging.error(f"{e}", exc_info=True)
