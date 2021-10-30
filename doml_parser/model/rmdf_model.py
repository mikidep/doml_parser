from typing import Optional
from dataclasses import dataclass

from .metadata import Metadata
from .provider import Provider
from .data_type import DataType
from .node_type import NodeType


@dataclass
class RMDFModel:
    metadata: Metadata
    provider: Optional[Provider]
    data_types: dict[str, DataType]
    node_types: dict[str, NodeType]

    def __post_init__(self) -> None:
        self._check()

    def _check(self) -> None:
        if self.provider is not None:
            self.provider._check()
        for dt in self.data_types.values():
            dt._check()
        for nt in self.node_types.values():
            nt._check()
