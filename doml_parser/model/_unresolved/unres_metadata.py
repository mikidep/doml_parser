from typing import Optional

from ..types import map_opt
from .unres_types import Unres

from .resolver import Resolver, ResolverCtx
from ..metadata import Metadata


class UnresMetadata:
    def __init__(self, md_dict: dict) -> None:
        self.version: str = md_dict["_version"]
        self.provider: Optional[Unres] = md_dict.get("_provider")
        self.description: Optional[str] = md_dict.get("_description")

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) -> Metadata:
        provider = map_opt(lambda pref:
                           resolver.resolve_provider(pref, ctx),
                           self.provider)
        return Metadata(self.version,
                        provider,
                        self.description)
