from typing import Tuple, Union
from dataclasses import dataclass

from . import types
from . import node_type as ntyp
from .interface import Interface
from .capability import Capability


@dataclass
class NodeTemplate:
    name: str
    type: 'ntyp.NodeType'
    properties: dict[str, Union['types.Expr', list['types.Expr']]]
    relationships: list[Tuple[str, 'NodeTemplate']]
    interfaces: dict[str, Interface]
    capabilities: dict[str, Capability]
