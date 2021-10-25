from dataclasses import dataclass

from .metadata import Metadata
from .property_def import PropertyDef
from .node_template import NodeTemplate
from .output import Output


@dataclass
class DOMLModel:
    metadata: Metadata
    input: dict[str, PropertyDef]
    node_templates: dict[str, NodeTemplate]
    output: dict[str, Output]
