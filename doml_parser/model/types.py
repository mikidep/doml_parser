from typing import Callable, TypeVar, Union, Optional, Literal, cast
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

from .data_type import DataType
from .node_type import NodeType
from .node_template import NodeTemplate
from .data import Data
from . import property_def as pdef
from ..errors import TypeError


Expr = Union[int, str, bool, float, Data, 'Function']

ValType = Union[Literal["String", "Integer", "Float", "Boolean"],
                DataType]


def valtype_name(vt: ValType) -> str:
    if type(vt) is DataType:
        return vt.name
    else:
        return cast(str, vt)


@dataclass
class TypingCtx:
    ntype: Optional[NodeType]
    ntpls: Optional[dict[str, NodeTemplate]]


def infer_type(e: Expr, ctx: TypingCtx) -> tuple[ValType, bool]:
    if type(e) is int:
        return "Integer", False
    elif type(e) is str:
        return "String", False
    elif type(e) is bool:
        return "Boolean", False
    elif type(e) is float:
        return "Float", False
    elif type(e) is Data:
        return e.type, False
    else:  # type(e) is Function
        return cast(Function, e).infer_type(ctx)


@dataclass
class Function(metaclass=ABCMeta):
    @abstractmethod
    def infer_type(self, ctx: TypingCtx) -> tuple[ValType, bool]:
        pass


@dataclass
class GetValue(Function):
    path: list[str]
    fsuper: bool = False

    def infer_type(self, ctx: TypingCtx) -> tuple[ValType, bool]:
        if ctx.ntype is not None and ctx.ntpls is not None:
            if self.fsuper:
                if ctx.ntype.extends is not None:
                    return ctx.ntype.extends.type_for_path(self.path,
                                                           "properties")
                else:
                    raise TypeError(
                        f"In node type {ctx.ntype.name}: get_value was used "
                        + "with 'super::' modifier, but node type "
                        + f"{ctx.ntype.name} does not extend any type."
                    )
            else:
                return ctx.ntype.type_for_path(self.path, "properties")
        else:
            raise TypeError(
                "get_value can only be used in the node_templates tag of a "
                + "node type."
            )


@dataclass
class GetAttribute(Function):
    path: list[str]

    def infer_type(self, ctx: TypingCtx) -> tuple[ValType, bool]:
        if ctx.ntpls is not None:
            head, *tail = self.path
            if (ntpl := ctx.ntpls.get(head)) is not None:
                return ntpl.type.type_for_path(tail)
            else:
                raise TypeError(
                    f"get_attribute: could not find node template '{head}'."
                )
        else:
            raise TypeError(
                "get_attribute can only be used within the context of a "
                + "node_templates tag."
            )


@dataclass
class Concat(Function):
    args: list[Expr]

    def infer_type(self, ctx: TypingCtx) -> tuple[ValType, bool]:
        return "String", False


@dataclass
class GetInput(Function):
    input: 'pdef.PropertyDef'

    def infer_type(self, ctx: TypingCtx) -> tuple[ValType, bool]:
        return self.input.type, False


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
