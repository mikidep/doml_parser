from dataclasses import dataclass

from . import node_type as ntyp


@dataclass
class Edge:
    name: str
    type: 'ntyp.NodeType'
    attribute: str
