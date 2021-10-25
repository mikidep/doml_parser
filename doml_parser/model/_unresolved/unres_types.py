from typing import Union, Literal, Tuple
from abc import ABCMeta, abstractmethod

from ...errors import InvalidRawValue, ReferenceNotFound, StructureError

from .resolver import Resolver, ResolverCtx
from ..types import (Function,
                     GetValue,
                     GetAttribute,
                     Concat,
                     GetInput,
                     Expr,
                     map_or_apply)
from .unres_doml_model import UnresDOMLModel
from .unres_data import resolve_expr

Unres = str

RawData = dict[str, Union['UnresExpr', list['UnresExpr']]]

UnresExpr = Union[int, str, bool, float,
                  RawData,
                  'UnresFunction']

UnresValType = Union[Literal["String", "Integer", "Float", "Boolean"],
                     Unres]


class UnresFunction(metaclass=ABCMeta):
    @abstractmethod
    def resolve(self, resolver: Resolver, ctx: ResolverCtx) \
            -> Function:
        pass


class UnresGetValue(UnresFunction):
    def __init__(self, path: list[str], fsuper: bool = False) -> None:
        super().__init__()
        self.path = path
        self.super = fsuper

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) \
            -> GetValue:
        pass


class UnresGetAttribute(UnresFunction):
    def __init__(self, path: list[str]) -> None:
        super().__init__()
        self.path = path

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) \
            -> GetAttribute:
        pass


def _attempt_resolve_expr(expr: UnresExpr,
                          etypes: list[UnresValType],
                          resolver: Resolver,
                          ctx: ResolverCtx) \
        -> Tuple[Expr, UnresValType]:
    for etype in etypes:
        try:
            return resolve_expr(expr,
                                etype,
                                resolver,
                                ctx), etype
        except TypeError:
            pass
    raise TypeError(f"Expression {expr} could not be resolved "
                    + "in any of the following types: "
                    + ", ".join(etypes) + ".")


class UnresConcat(UnresFunction):
    def __init__(self, args: list[UnresExpr]) -> None:
        super().__init__()
        self.args = args

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) \
            -> Concat:
        args = [_attempt_resolve_expr(arg,
                                      ["String", "Integer"],
                                      resolver,
                                      ctx)[0]
                for arg in self.args]
        return Concat(args)


class UnresGetInput(UnresFunction):
    def __init__(self, input: str):
        self.input = input

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) \
            -> GetInput:
        if type(ctx.unres_model) is UnresDOMLModel:
            if (i := ctx.unres_model.input.get(self.input)) is not None:
                return GetInput(i.resolve(resolver, ctx))
            else:
                raise ReferenceNotFound(f"No input named {self.input}.")
        else:
            raise StructureError("Cannot use get_input in an RMDF model.")


def raw_to_unres_expr(rv) -> UnresExpr:
    if isinstance(rv, (int, str, bool, float)):
        return rv
    elif type(rv) is dict:
        if "get_value" in rv:
            path: str = rv["get_value"]
            super = False
            if path.startswith("super::"):
                super = True
                path = path[7:]
            return UnresGetValue(path.split("."), super)
        elif "get_attribute" in rv:
            path: str = rv["get_attribute"]
            return UnresGetAttribute(path.split("."))
        elif "concat" in rv:
            args: list = rv["concat"]
            return UnresConcat([raw_to_unres_expr(arg) for arg in args])
        elif "get_input" in rv:
            return UnresGetInput(rv["get_input"])
        else:
            return {p: map_or_apply(raw_to_unres_expr, v)
                    for p, v in rv.items()}
    else:
        raise InvalidRawValue(f"Value of type {type(rv).__name__} "
                              + "is not a valid DOML value.")
