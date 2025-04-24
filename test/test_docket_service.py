from model.service import Service
import pytest

docket_url = "https://www.courtlistener.com/docket/69746454/20/state-of-maryland-v-usda/"
bad_url = "chickennuggets.com"

def test_extract_docket_id():
    docket_id = Service._extract_docket_id(docket_url)
    assert docket_id == "69746454"

def test_extract_docket_id_error():
    with pytest.raises(Exception):
        Service._extract_docket_id(bad_url)

def test_create_docket_request_url():
    req_url = Service._create_docket_request_url(docket_id="69746454")
    assert req_url == "https://www.courtlistener.com/api/rest/v4/dockets/69746454"

def test_create_entries_request_url():
    req_url = Service._create_entries_request_url(docket_id="69746454")
    assert req_url == "https://www.courtlistener.com/api/rest/v4/docket-entries/?docket=69746454"