from typing import Optional
from dataclasses import dataclass

from . import property_def as pdef


@dataclass
class DataType:
    name: str
    description: Optional[str]
    extends: Optional['DataType']
    prop_defs: dict[str, 'pdef.PropertyDef']
