import pytz
from libs import datetime_formatter as dtf
from libs import json_util as ju
from functools import cached_property
from dataclasses import asdict, dataclass, fields
from typing import ClassVar

JSON_RESPONSE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Entire Docket (one case)
@dataclass
class Docket:
    id:int
    case_name: str
    date_modified: str
    date_filed: str
    assigned_to_str: str
    docket_number:str
    court_id:str
    is_appeal:bool
    wanted_fields: ClassVar = ["id", 
                "case_name", 
                "date_modified", 
                "date_filed", 
                "assigned_to_str", 
                "docket_number", 
                "court_id", 
                "appeal_from"]

    # @staticmethod
    # def _format_dt_str(dt_str):
    #     central_tz = pytz.timezone('US/Central')
    #     dt = dtf.str_to_dt(dt_str, JSON_RESPONSE_DATETIME_FORMAT, central_tz)
    #     new_dt_format = "%A %b %d at %I %p %Z"
    #     return dtf.format_dt(dt, new_dt_format)

    @staticmethod 
    def change_appeal_field(json:dict) -> dict:
        if "appeal_from" in json:
            appeal_from = json.pop("appeal_from")
            is_appeal = True if appeal_from else False
            json["is_appeal"] = is_appeal
        else:
            json["is_appeal"] = False
        return json
    
    def obj_to_dict(self) -> dict:
        return asdict(self) # class instance -> dict (instance vars only)

    @classmethod
    def dict_to_obj(cls, json:dict) -> "Docket":
        shortened_json = ju.simplify_json(json, cls.wanted_fields)
        docketified_json = Docket.change_appeal_field(shortened_json)
        return cls(**docketified_json)