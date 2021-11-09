from typing import Literal, Optional
from dataclasses import dataclass

from .property_def import PropertyDef
from . import node_template as ntpl
from .edge import Edge

from .data_type import DataType
from . import types


@dataclass
class NodeType:
    name: str
    description: str
    alias: Optional[str]
    extends: Optional['NodeType']
    prop_defs: dict[str, PropertyDef]
    node_templates: dict[str, 'ntpl.NodeTemplate']
    edges: dict[str, Edge]

    def inherits_from(self, nt: 'NodeType') -> bool:
        return self == nt \
               or (self.extends is not None and self.extends.inherits_from(nt))

    # Returns type for path and whether to expect a multiple value
    def type_for_path(
        self,
        path: list[str],
        search: Literal["properties", "all"] = "all"
    ) -> tuple['types.ValType', bool]:
        head, *tail = path
        if not tail:
            if (pd := self.prop_defs.get(head)) is not None:
                return pd.type, pd.multiple
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
            elif search == "all" \
                    and (nt := self.node_templates.get(head)) is not None:
                return nt.type.type_for_path(tail)
            else:
                if search == "properties":
                    scope = "property"
                else:  # search == "all"
                    scope = "property or node template"
                raise TypeError(
                    f"Cannot evaluate path '{'.'.join(path)}' in node type "
                    + f"{self.name}: no {scope} named '{head}'."
                )

    def _check(self) -> None:
        if self.extends is not None:
            self.extends._check()

        for pd in self.prop_defs.values():
            pd._check(types.TypingCtx(None, None))

        ctx = types.TypingCtx(self, self.node_templates)
        for nt in self.node_templates.values():
            nt._check(ctx)

        for e in self.edges.values():
            e._check()
