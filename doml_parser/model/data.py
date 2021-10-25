from typing import Union
from dataclasses import dataclass

from . import types
from .data_type import DataType


@dataclass
class Data:
    type: DataType
    properties: dict[str, Union['types.Expr', list['types.Expr']]]
