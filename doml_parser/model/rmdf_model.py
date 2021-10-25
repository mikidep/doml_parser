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
