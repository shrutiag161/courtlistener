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
# DOCKET_FIELDS = "docket_fields_to_include.txt"

def read_input_files() -> tuple[list[str], str]:
    try:
        docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True, allow_empty_file=False) 
        api_token = fr.read_file_as_string(TOKEN_FILE, allow_empty_file=False) 
        return docket_urls, api_token
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(1)

def write_to_json(file_path:str, obj: dict | list):
    with open(file_path, 'w') as output_file:
        json.dump(obj, output_file, indent=4, ensure_ascii=False)

def write_docket_to_json(docket: Docket, *, output_dir:str):
    docket_id = docket.id
    file_path = f"{output_dir}docket_{docket_id}.json"
    docket_dict = docket.to_dict()
    write_to_json(file_path, docket_dict)

def write_entries_to_json(entries: list, docket_id:str, *, output_dir:str):
    entries_dicts = []
    file_path = f"{output_dir}docket_{docket_id}_entries.json"
    for e in entries:
        entry = DocketEntry(e)
        entry_dict = entry.to_dict()
        entry_dict["docket_id"] = docket_id
        entries_dicts.append(entry_dict)
    write_to_json(file_path, entries_dicts)


def main():
    docket_urls, api_token = read_input_files()
    service = DocketService(api_token)
    for url in docket_urls:
        docket_json = service.get_docket_json(url)
        docket = Docket(docket_json)
        write_docket_to_json(docket, output_dir="./model/jsons/")
        docket_entries = service.get_entries(url)
        write_entries_to_json(docket_entries, docket.id, output_dir="./model/jsons/")

if __name__ == "__main__":
    main()


