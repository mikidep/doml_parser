from typing import Tuple, Union

from ..types import map_or_apply

from . import unres_types as ut
from .unres_interface import UnresInterface
from .unres_capability import UnresCapability

from . import resolver as r
from ..node_template import NodeTemplate
from .unres_data import resolve_expr
from ...errors import TypeError


class UnresNodeTemplate:
    def __init__(self, name: str, nt_dict: dict) -> None:
        self.name = name
        self.type: ut.Unres = nt_dict["type"]
        self.properties: dict[str, Union[ut.UnresExpr, list[ut.UnresExpr]]] \
            = {pname: map_or_apply(ut.raw_to_unres_expr, pv)
               for pname, pv in nt_dict.get("properties", {}).items()}
        r_dict = nt_dict.get("relationships", {})
        self.relationships: list[Tuple[str, ut.Unres]] \
            = [(rname, rnode)
               for rname in r_dict
               for rnode in (
                   r_dict[rname]
                   if type(r_dict[rname]) is list
                   else [r_dict[rname]]
                )]
        self.interfaces: dict[str, UnresInterface] \
            = {iname: UnresInterface(iname, idict)
               for iname, idict in nt_dict.get("interfaces", {}).items()}
        self.capabilities: dict[str, UnresCapability] \
            = {cname: UnresCapability(cname, cdict)
               for cname, cdict in nt_dict.get("capabilities", {}).items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> NodeTemplate:
        # Resolver.resolve_node_type will forget the node_templates in ctx
        ntype = resolver.resolve_node_type(self.type,
                                           ctx)
        properties = {}
        for pname in self.properties:
            if pname in ntype.prop_defs:
                pdef = ntype.prop_defs[pname]
                properties[pname] = map_or_apply(
                    lambda pval: resolve_expr(pval,
                                              pdef.type,
                                              resolver,
                                              ctx),
                    self.properties[pname]
                )
            else:
                raise TypeError(f"Undefined property '{pname}' in "
                                + f"node template of type {self.type}.")
        relationships = [
            (rname, resolver.resolve_node_template(rntref, ctx))
            for rname, rntref in self.relationships
        ]
        interfaces = {
            iname: i.resolve(resolver, ctx)
            for iname, i in self.interfaces.items()
        }
        capabilities = {
            cname: c.resolve(resolver, ctx)
            for cname, c in self.capabilities.items()
        }
        return NodeTemplate(self.name,
                            ntype,
                            properties,
                            relationships,
                            interfaces,
                            capabilities)
