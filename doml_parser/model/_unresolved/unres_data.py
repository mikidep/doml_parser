from typing import cast

from . import unres_types as ut
from ..types import Expr, map_or_apply
from . import resolver as r
from ..data import Data
from ..data_type import DataType
from ...errors import TypeError


class UnresData:
    def __init__(self,
                 dtype: 'ut.Unres',
                 properties: 'ut.RawData') -> None:
        self.type = dtype
        self.properties = properties

    def resolve(self,
                resolver: 'r.Resolver',
                ctx: 'r.ResolverCtx') -> Data:
        dtype = resolver.resolve_data_type(self.type, ctx)
        properties = {}
        for pname in self.properties:
            if pname in dtype.prop_defs:
                pdef = dtype.prop_defs[pname]
                if type(pdef.type) is str:
                    utype = pdef.type
                else:
                    pdt = cast(DataType, pdef.type)
                    utype = pdt.name
                properties[pname] = map_or_apply(
                    lambda pval: resolve_expr(pval,
                                              utype,
                                              resolver,
                                              ctx),
                    self.properties[pname]
                )
            else:
                raise TypeError(f"Undefined property {pname} in "
                                + f"data object of type {self.type}.")

        return Data(dtype, properties)


def resolve_expr(expr: 'ut.UnresExpr',
                 etype: 'ut.UnresValType',
                 resolver: 'r.Resolver',
                 ctx: 'r.ResolverCtx') -> Expr:
    def check_type(v, t, tname):
        if type(v) is not t and not isinstance(v, ut.UnresFunction):
            raise TypeError(f"Expected value of type {tname}, "
                            + f"found value {v} of type {type(v).__name__}.")

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
    else:  # type(expr) is dict
        data = UnresData(etype, expr)
        return data.resolve(resolver, ctx)
