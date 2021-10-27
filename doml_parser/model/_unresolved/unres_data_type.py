from typing import Optional

from ..types import map_opt

from . import unres_types as ut
from .unres_property_def import UnresPropertyDef

from . import resolver as r
from ..data_type import DataType


class UnresDataType:
    def __init__(self, name: str, dt_dict: dict) -> None:
        self.name = name
        self.description: Optional[str] = dt_dict.get("description")
        self.extends: Optional[ut.Unres] = dt_dict.get("extends")
        self.prop_defs: dict[str, UnresPropertyDef] \
            = {pdname: UnresPropertyDef(pdname, pddict)
               for pdname, pddict in dt_dict["properties"].items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> DataType:
        extends = map_opt(lambda dtref:
                          resolver.resolve_data_type(dtref, ctx),
                          self.extends)
        prop_defs = {pdname: pd.resolve(resolver, ctx)
                     for pdname, pd in self.prop_defs.items()}

        if extends is not None:
            prop_defs |= extends.prop_defs

        return DataType(self.name,
                        self.description,
                        extends,
                        prop_defs)
