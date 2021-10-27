from typing import Union

from . import unres_types as ut

from . import resolver as r
from ..node_type import NodeType
from ..ntpl_property import NTplProperty
from ..types import map_or_apply
from .unres_data import resolve_expr


class UnresNTplProperty:
    def __init__(self,
                 path: list[str],
                 value: Union['ut.UnresExpr', list['ut.UnresExpr']]) -> None:
        assert len(path) > 0
        self.path = path
        self.value = value

    def resolve(self,
                ntype: NodeType,
                resolver: 'r.Resolver',
                ctx: 'r.ResolverCtx') -> NTplProperty:
        ptype = ntype.type_for_path(self.path)
        value = map_or_apply(
                    lambda pval: resolve_expr(pval,
                                              ptype,
                                              resolver,
                                              ctx),
                    self.value
                )
        return NTplProperty(self.path, ptype, value)
