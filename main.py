import docket_request as dr
from libs import file_reader as fr
import logging
import sys

# https://www.courtlistener.com/docket/69746454/20/state-of-maryland-v-usda/

DOCKET_URLS_FILE = "docket_urls.txt"

docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True) 
if not docket_urls: 
    sys.exit(f"{DOCKET_URLS_FILE} is empty")

for docket_url in docket_urls:
    print(f"Docket: {docket_url}")
    try:    
        case_info = dr.get_docket_json(docket_url)
        print(f"Case: {dr.get_case_name(case_info)}")
        print(f"Last Updated {dr.get_last_updated_timestamp(case_info)}\n")
    except Exception as e:
        logging.error(f"{e}", exc_info=True)
