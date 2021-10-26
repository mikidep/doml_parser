from . import unres_types as ut

from . import resolver as r
from ..output import Output


class UnresOutput:
    def __init__(self,
                 name: str,
                 o_dict: dict) -> None:
        self.name = name
        self.type: ut.UnresValType = o_dict["type"]
        self.value: ut.UnresExpr = ut.raw_to_unres_expr(o_dict["value"])

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Output:
        vtype = ut.resolve_val_type(self.type, resolver, ctx)
        return Output(
            self.name,
            vtype,
            ut.resolve_expr(self.value, vtype, resolver, ctx)
        )
