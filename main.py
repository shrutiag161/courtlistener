from model.service import Service
from model.docket import Docket
from model.docket_entry import DocketEntry
from libs import file_reader as fr
import logging
import sys
import json

# rate limiting
# pathlib

# explain the service api code
# is docket processor necessary 
# fetch or get
# should rate limiting go in _fetch_all_paginated_entries or _get_response
# do files i import have to be classes

DOCKET_URLS_FILE = "docket_urls.txt"
TOKEN_FILE = "token.txt"
OUTPUT_DIR = "./model/jsons/"

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

def write_docket_to_json(docket: Docket, output_dir:str):
    docket_id = docket.id
    file_path = f"{output_dir}docket_{docket_id}.json"
    write_to_json(file_path, docket.obj_to_dict())

def write_docket_entries_to_json(docket_entries: list[DocketEntry], docket_id, output_dir:str):
    file_path = f"{output_dir}docket_{docket_id}_entries.json"
    docket_entry_jsons = [entry.obj_to_dict() for entry in docket_entries]
    write_to_json(file_path, docket_entry_jsons)

def process_docket(docket_json:dict, output_dir:str) -> None:
    docket = Docket.dict_to_obj(docket_json)
    write_docket_to_json(docket, output_dir)

def process_entries(entry_jsons:list[dict], docket_id, output_dir:str) -> None:
    docket_entries = [DocketEntry.dict_to_obj(ej, docket_id) for ej in entry_jsons]
    write_docket_entries_to_json(docket_entries, docket_id, output_dir)

def main():
    docket_urls, api_token = read_input_files()
    service = Service(api_token)
    for url in docket_urls:
        docket_json = service.get_docket_json(url)
        process_docket(docket_json, OUTPUT_DIR)
        # entry_jsons = service.get_entries(url)
        # process_entries(entry_jsons, docket_json["id"], OUTPUT_DIR)

if __name__ == "__main__":
    main()


