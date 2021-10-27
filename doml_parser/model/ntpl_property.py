from typing import Union
from dataclasses import dataclass

from . import types


@dataclass
class NTplProperty:
    path: list[str]
    type: 'types.ValType'
    value: Union['types.Expr', list['types.Expr']]
