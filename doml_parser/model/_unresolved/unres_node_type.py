from typing import Optional

from . import unres_types as ut
from .unres_property_def import UnresPropertyDef
from .unres_node_template import UnresNodeTemplate
from .unres_edge import UnresEdge

from . import resolver as r
from ..node_type import NodeType
from ..types import map_opt


class UnresNodeType:
    def __init__(self, name: str, nt_dict: dict) -> None:
        self.name = name
        self.description: str = nt_dict["description"]
        self.alias: Optional[str] = nt_dict.get("alias")
        self.extends: Optional[ut.Unres] = nt_dict.get("extends")
        self.prop_defs: dict[str, UnresPropertyDef] \
            = {pdname: UnresPropertyDef(pdname, pddict)
               for pdname, pddict in nt_dict.get("properties", {}).items()}
        self.node_templates: dict[str, UnresNodeTemplate] \
            = {ntname: UnresNodeTemplate(ntname, ntdict)
               for ntname, ntdict in nt_dict.get("node_templates", {}).items()}
        self.edges: dict[str, UnresEdge] \
            = {ename: UnresEdge(ename, edict)
               for ename, edict in nt_dict.get("edges", {}).items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> NodeType:
        extends = map_opt(lambda ref: resolver.resolve_node_type(ref, ctx),
                          self.extends)
        edges = {ename: edge.resolve(resolver, ctx)
                 for ename, edge in self.edges.items()}
        ntctx = r.ResolverCtx(ctx.unres_model,
                              # ctx.node_type,
                              r.NodeTplCtx(self.node_templates, {}))
        node_templates = {ntname: nt.resolve(resolver, ctx)
                          for ntname, nt in self.node_templates.items()}
        prop_defs = {pdname: pd.resolve(resolver, ntctx)
                     for pdname, pd in self.prop_defs.items()}
        return NodeType(self.name,
                        self.description,
                        self.alias,
                        extends,
                        prop_defs,
                        node_templates,
                        edges)
