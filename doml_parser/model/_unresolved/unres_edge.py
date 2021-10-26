from . import unres_types as ut

from . import resolver as r
from ..edge import Edge


class UnresEdge:
    def __init__(self, name: str, e_dict: dict) -> None:
        self.name = name
        self.type: ut.Unres = e_dict["type"]
        self.attribute: str = e_dict["attribute"]

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Edge:
        return Edge(self.name,
                    resolver.resolve_node_type(self.type, ctx),
                    self.attribute)
