from dataclasses import dataclass

from .metadata import Metadata
from .property_def import PropertyDef
from .node_template import NodeTemplate
from .output import Output
from .types import TypingCtx


@dataclass
class DOMLModel:
    metadata: Metadata
    input: dict[str, PropertyDef]
    node_templates: dict[str, NodeTemplate]
    output: dict[str, Output]

    def __post_init__(self) -> None:
        self._check()

    def _check(self) -> None:
        for i in self.input.values():
            i._check(TypingCtx(None, None))
        ctx = TypingCtx(None, self.node_templates)
        for ntpl in self.node_templates.values():
            ntpl._check(ctx)
        for o in self.output.values():
            o._check(ctx)
