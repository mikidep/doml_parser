from typing import Callable, TypeVar, Union, Optional, Literal, cast
from dataclasses import dataclass

from .data_type import DataType
from .data import Data
from . import property_def as pdef
from . import node_template as ntpl


Expr = Union[int, str, bool, float, Data, 'Function']

ValType = Union[Literal["String", "Integer", "Float", "Boolean"],
                DataType]


@dataclass
class Function:
    pass


@dataclass
class GetValue(Function):
    path: list[str]
    fsuper: bool = False


@dataclass
class GetAttribute(Function):
    node_template: 'ntpl.NodeTemplate'
    path: list[str]


@dataclass
class Concat(Function):
    args: list[Expr]


@dataclass
class GetInput(Function):
    input: 'pdef.PropertyDef'


_A = TypeVar("_A")
_B = TypeVar("_B")


def map_opt(f: Callable[[_A], _B], opt: Optional[_A]) -> Optional[_B]:
    return None if opt is None else f(opt)


def map_or_else(f: Callable[[_A], _B],
                default: _B,
                opt: Optional[_A]) -> _B:
    return default if opt is None else f(opt)


def map_or_apply(f: Callable[[_A], _B], v: Union[_A, list[_A]]) \
        -> Union[_B, list[_B]]:
    if type(v) is list:
        vv = cast(list[_A], v)
        return [f(x) for x in vv]
    else:
        return f(v)
