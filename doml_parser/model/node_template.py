from typing import Tuple
from dataclasses import dataclass

from . import node_type as ntyp
from .ntpl_property import NTplProperty
from .interface import Interface
from .capability import Capability


@dataclass
class NodeTemplate:
    name: str
    type: 'ntyp.NodeType'
    properties: list[NTplProperty]
    relationships: list[Tuple[str, 'NodeTemplate']]
    interfaces: dict[str, Interface]
    capabilities: dict[str, Capability]
