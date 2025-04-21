import model.docket as d
from model.docket_service import DocketService
from model.docket import Docket
from model.docket_entry import DocketEntry
from libs import file_reader as fr
from libs import rest_api as ra
import logging
import sys
import pprint
import json

DOCKET_URLS_FILE = "docket_urls.txt"
TOKEN_FILE = "token.txt"
DOCKET_FIELDS = "docket_fields_to_include.txt"

def read_input_files() -> tuple[list[str], str]:
    try:
        docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True, allow_empty_file=False) 
        api_token = fr.read_file_as_string(TOKEN_FILE, allow_empty_file=False)
        docket_fields = fr.read_file_as_list(DOCKET_FIELDS, ignore_blank_lines=True, allow_empty_file=True) 
        return docket_urls, api_token, docket_fields
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(1)

def write_docket_to_json_file(docket:dict):
    if "id" not in docket:
        raise ValueError("No docket id!!")
    with open(f"./model/jsons/docket_{docket['id']}.json", 'w') as tempjson:
        json.dump(docket, tempjson, indent=4)

def write_entries_to_json_file(id, entries):
    with open(f"./model/jsons/docket_{id}_entries.json", 'w') as tempjson:
        json.dump(entries, tempjson, indent=4)

def main():
    docket_urls, api_token, docket_fields = read_input_files()
    service = DocketService(api_token)
    for url in docket_urls:
        docket_json = service.get_docket_json(url, fields=docket_fields)
        write_docket_to_json_file(docket_json)
        # docket_entries = service.get_entries(url)
        # id = docket_json.get("id")
        # write_entries_to_json_file(id, docket_entries)

if __name__ == "__main__":
    main()


