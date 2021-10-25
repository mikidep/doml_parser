from dataclasses import dataclass

from . import node_type as ntyp


@dataclass
class Capability:
    name: str
    default_instances: int
    targets: list['ntyp.NodeType']
