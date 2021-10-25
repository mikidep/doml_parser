from typing import Optional
from dataclasses import dataclass

from .property_def import PropertyDef
from .node_template import NodeTemplate
from .edge import Edge


@dataclass
class NodeType:
    name: str
    description: str
    alias: Optional[str]
    extends: Optional['NodeType']
    prop_defs: dict[str, PropertyDef]
    node_templates: dict[str, NodeTemplate]
    edges: dict[str, Edge]
