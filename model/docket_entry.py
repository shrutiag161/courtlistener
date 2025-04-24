from functools import cached_property
from typing import ClassVar
from dataclasses import asdict, dataclass, fields
from libs import json_util as ju

# One single docket entry
@dataclass
class DocketEntry:
    id: int
    docket_id:int
    date_filed: str
    date_modified: str
    entry_number: int
    description: str
    wanted_fields: ClassVar = ["id",
                        "date_filed", 
                        "date_modified",
                        "entry_number",
                        "description"]
    
    def obj_to_dict(self) -> dict:
        return asdict(self) # class instance -> dict (instance vars only)

    @classmethod
    def dict_to_obj(cls, json:dict, docket_id) -> "DocketEntry":
        shortened_json = ju.simplify_json(json, cls.wanted_fields)
        docketified_json = ju.add_field(shortened_json, "docket_id", docket_id)
        return cls(**docketified_json)