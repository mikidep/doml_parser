from typing import cast

from . import unres_types as ut
from ..types import Expr, ValType, map_or_apply
from . import resolver as r
from ..data import Data
from ..data_type import DataType
from ...errors import TypeError


class UnresData:
    def __init__(self,
                 dtype: DataType,
                 properties: 'ut.RawData') -> None:
        self.type = dtype
        self.properties = properties

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Data:
        properties = {}
        for pname in self.properties:
            if pname in self.type.prop_defs:
                pdef = self.type.prop_defs[pname]
                properties[pname] = map_or_apply(
                    lambda pval: resolve_expr(pval,
                                              pdef.type,
                                              resolver,
                                              ctx),
                    self.properties[pname]
                )
            else:
                raise TypeError(f"Undefined property '{pname}' in "
                                + f"data object of type {self.type}.")

        return Data(self.type, properties)


def resolve_expr(expr: 'ut.UnresExpr',
                 etype: ValType,
                 resolver: 'r.Resolver',
                 ctx: 'r.ResolverCtx') -> Expr:
    def check_type(v, t, tname) -> None:
        if type(v) is not t and not isinstance(v, ut.UnresFunction):
            raise TypeError(f"Expected value of type {tname}, "
                            + f"found value '{v}' of type {type(v).__name__}.")

    expected_type = (str if etype == "String"
                     else int if etype == "Integer"
                     else float if etype == "Float"
                     else bool if etype == "Boolean"
                     else dict)
    check_type(expr, expected_type, etype)
    if isinstance(expr, (str, int, float, bool)):
        return expr
    elif isinstance(expr, ut.UnresFunction):
        return expr.resolve(resolver, ctx)
    else:
        etype = cast(DataType, etype)
        data = UnresData(etype, expr)
        return data.resolve(resolver, ctx)
