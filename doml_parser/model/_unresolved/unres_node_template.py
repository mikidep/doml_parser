from typing import Tuple, Union

from ..types import map_or_apply

from . import unres_types as ut
from .unres_interface import UnresInterface
from .unres_capability import UnresCapability


class UnresNodeTemplate:
    def __init__(self, name: str, nt_dict: dict) -> None:
        self.name = name
        self.type: ut.Unres = nt_dict["type"]
        self.properties: dict[str, Union[ut.UnresExpr, list[ut.UnresExpr]]] \
            = {k: map_or_apply(ut.raw_to_unres_expr, v)
               for k, v in nt_dict.get("properties", {}).items()}
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
