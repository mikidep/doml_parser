from .unres_property_def import UnresPropertyDef

from . import resolver as r
from ..provider import Provider


class UnresProvider:
    def __init__(self, p_dict: dict) -> None:
        self.alias: str = p_dict["alias"]
        self.features: dict[str, UnresPropertyDef] \
            = {pname: UnresPropertyDef(pname,
                                       pd,
                                       f"provider {self.alias}",
                                       False)
               for pname, pd in p_dict["features"].items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Provider:
        return Provider(
            self.alias,
            {fname: f.resolve(resolver, ctx)
             for fname, f in self.features.items()}
        )
