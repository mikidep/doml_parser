from typing import Optional, Union
from dataclasses import dataclass

from .types import Expr, ValType


@dataclass
class PropertyDef:
    name: str
    type: ValType
    description: Optional[str]
    required: bool
    multiple: bool
    default: Optional[Union[Expr, list[Expr]]]
