from typing import Optional

from ..types import map_opt
from .unres_model import UnresModel
from .unres_metadata import UnresMetadata
from .unres_provider import UnresProvider
from .unres_data_type import UnresDataType
from .unres_node_type import UnresNodeType

from ..rmdf_model import RMDFModel
from .resolver import Resolver, ResolverCtx


class UnresRMDFModel(UnresModel):
    def __init__(self, rmdf_dict: dict) -> None:
        super().__init__(rmdf_dict.get("imports", []))
        self.metadata: UnresMetadata = UnresMetadata(rmdf_dict["metadata"])
        self.provider: Optional[UnresProvider] \
            = map_opt(UnresProvider, rmdf_dict.get("provider"))
        self.data_types: dict[str, UnresDataType] \
            = {dtname: UnresDataType(dtname, dtdict)
               for dtname, dtdict in rmdf_dict.get("data_types", {}).items()}
        self.node_types: dict[str, UnresNodeType] \
            = {ntname: UnresNodeType(ntname, ntdict)
               for ntname, ntdict in rmdf_dict.get("node_types", {}).items()}

    def resolve(self, resolver: Resolver, ctx: ResolverCtx) -> RMDFModel:
        metadata = self.metadata.resolve(resolver, ctx)
        provider = map_opt(lambda p: p.resolve(resolver, ctx),
                           self.provider)
        data_types = {dtname: dt.resolve(resolver, ctx)
                      for dtname, dt in self.data_types.items()}
        node_types = {ntname: nt.resolve(resolver, ctx)
                      for ntname, nt in self.node_types.items()}
        return RMDFModel(metadata,
                         provider,
                         data_types,
                         node_types)
