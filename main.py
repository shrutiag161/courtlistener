import docket as d
from docket_service import DocketService
from libs import file_reader as fr
from libs import rest_api as ra
import logging
import sys
import pprint
import json

DOCKET_URLS_FILE = "docket_urls.txt"
TOKEN_FILE = "token.txt"

def read_input_files() -> tuple[list[str], str]:
    try:
        docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True, allow_empty_file=False) 
        api_token = fr.read_file_as_string(TOKEN_FILE, allow_empty_file=False)
        return docket_urls, api_token
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(1)

def write_to_json(**docket_info):
    if "id" not in docket_info:
        raise ValueError("No docket id!!")
    with open(f"{docket_info['id']}.json", 'w') as tempjson:
        json.dump(docket_info, tempjson, indent=4)

def main():
    docket_urls, api_token = read_input_files()
    service = DocketService(api_token)
    for url in docket_urls:
        docket_json = service.get_docket_json(url)
        # docket = Docket(docket_json)
        # save_to_docket_db(docket.docket_id, docket.case_name, docket.date_modified)
        docket_entries = service.get_entries(url)
        for e in docket_entries:
            # entry = DocketEntry(e)
            # save_to_entry_db(docket.docket_id, entry)
        
        # with d.Docket(url, api_token) as docket:
        #     docket_info = {
        #         "id": docket.docket_id,
        #         "case_name": docket.case_name, 
        #         "last_updated": docket.date_modified, 
        #         "entries": docket.entries
        #     }
        # write_to_json(**docket_info)

if __name__ == "__main__":
    main()


