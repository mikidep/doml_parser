from . import unres_types as ut

from . import resolver as r
from ..capability import Capability


class UnresCapability:
    def __init__(self, name: str, c_dict: dict) -> None:
        self.name = name
        self.default_instances: int = c_dict["default_instances"]
        self.targets: list[ut.Unres] = c_dict.get("targets", [])

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Capability:
        return Capability(self.name,
                          self.default_instances,
                          [resolver.resolve_node_type(t, ctx)
                           for t in self.targets])
