import docket as d
from libs import file_reader as fr
import logging
import sys

DOCKET_URLS_FILE = "docket_urls.txt"
TOKEN_FILE = "token.txt"

def read_input_files():
    try:
        docket_urls = fr.read_file_as_list(DOCKET_URLS_FILE, ignore_blank_lines=True, allow_empty_file=False) 
        api_token = fr.read_file_as_string(TOKEN_FILE, allow_empty_file=False)
        return docket_urls, api_token
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(1)

def docket_info(docket_url, api_token):
    print(f"Docket: {docket_url}")
    try:
        docket = d.Docket(docket_url, api_token)
        print(f"Case: {docket.case_name()}")
        print(f"Last Updated: {docket.date_modified()}\n")
    except Exception as e:
        logging.error(f"{e}", exc_info=True)

def main():
    docket_urls, api_token = read_input_files()
    for url in docket_urls:
        docket_info(url, api_token)

if __name__ == "__main__":
    main()


