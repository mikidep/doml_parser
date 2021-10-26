from typing import Optional, Union
from dataclasses import dataclass

from . import types


@dataclass
class PropertyDef:
    name: str
    type: 'types.ValType'
    description: Optional[str]
    required: bool
    multiple: bool
    default: Optional[Union['types.Expr', list['types.Expr']]]
