from dataclasses import dataclass

from .types import Expr, ValType


@dataclass
class Output:
    name: str
    type: ValType
    value: Expr
