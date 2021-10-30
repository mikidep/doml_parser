from typing import Optional, Union

from ..types import map_opt, map_or_apply, Expr

from . import unres_types as ut

from . import resolver as r
from ..property_def import PropertyDef
from .unres_data import resolve_expr


class UnresPropertyDef:
    def __init__(self,
                 name: str,
                 pd_dict: dict,
                 context: str,
                 is_input: bool) -> None:
        self.name = name
        self.type: ut.UnresValType = pd_dict["type"]
        self.description: Optional[str] = pd_dict.get("description")
        self.required: bool = pd_dict.get("required", False)
        self.multiple: bool = pd_dict.get("multiple", False)
        self.default: Optional[Union[ut.UnresExpr, list[ut.UnresExpr]]] \
            = map_opt(lambda d: map_or_apply(ut.raw_to_unres_expr, d),
                      pd_dict.get("default"))
        self.context = context
        self.is_input = is_input

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> PropertyDef:
        pd_type = ut.resolve_val_type(self.type, resolver, ctx)

        def resolve_expr_(v: ut.UnresExpr) -> Expr:
            return resolve_expr(v,
                                pd_type,
                                resolver,
                                ctx)

        default = map_opt(
            lambda sd: map_or_apply(resolve_expr_, sd),
            self.default
        )

        return PropertyDef(self.name,
                           pd_type,
                           self.description,
                           self.required,
                           self.multiple,
                           default,
                           self.context,
                           self.is_input)
