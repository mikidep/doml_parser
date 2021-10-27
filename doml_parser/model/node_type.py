from typing import Optional
from dataclasses import dataclass

from .property_def import PropertyDef
from . import node_template as ntpl
from .edge import Edge

from .data_type import DataType


@dataclass
class NodeType:
    name: str
    description: str
    alias: Optional[str]
    extends: Optional['NodeType']
    prop_defs: dict[str, PropertyDef]
    node_templates: dict[str, 'ntpl.NodeTemplate']
    edges: dict[str, Edge]

    def type_for_path(self, path: list[str]):
        head, *tail = path
        if not tail:
            if (pd := self.prop_defs.get(head)) is not None:
                return pd.type
            else:
                raise TypeError(f"Undefined property '{head}' in "
                                + f"node type {self.name}.")
        else:
            if (pd := self.prop_defs.get(head)) is not None:
                if pd.multiple:
                    raise TypeError(
                        f"Cannot evaluate path '{'.'.join(path)}' in node "
                        + f"type {self.name}: property '{head}' is a "
                        + "multiple value property."
                    )
                if type(pd.type) is DataType:
                    return pd.type.type_for_path(tail)
                else:
                    raise TypeError(
                        f"Cannot evaluate path '{'.'.join(path)}' in node "
                        + f"type {self.name}: property '{head}' is of "
                        + f"scalar type '{pd.type}'."
                    )
            elif (nt := self.node_templates.get(head)) is not None:
                return nt.type.type_for_path(tail)
            else:
                raise TypeError(
                    f"Cannot evaluate path '{'.'.join(path)}' in node type "
                    + f"{self.name}: no property or node template named "
                    + f"'{head}'."
                )
