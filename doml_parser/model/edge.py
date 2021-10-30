from dataclasses import dataclass

from . import node_type as ntyp
# from ..errors import TypeError


@dataclass
class Edge:
    name: str
    type: 'ntyp.NodeType'
    attribute: str

    def _check(self) -> None:
        # if self.attribute not in self.type.prop_defs:
        #     raise TypeError(
        #         f"In edge '{self.name}': property '{self.attribute}' not "
        #         + f"defined in node type {self.type.name}."
        #     )
        # if self.type.prop_defs[self.attribute].type != "String":
        #     raise TypeError(
        #         f"In edge '{self.name}': property '{self.attribute}' "
        #         + f"defined in node type {self.type.name} should be of type "
        #         + "String."
        #     )
        pass
