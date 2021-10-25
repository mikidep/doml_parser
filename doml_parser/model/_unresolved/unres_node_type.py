from typing import Optional

from . import unres_types as ut
from .unres_property_def import UnresPropertyDef
from .unres_node_template import UnresNodeTemplate
from .unres_edge import UnresEdge


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
