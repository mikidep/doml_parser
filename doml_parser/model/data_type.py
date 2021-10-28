from typing import Optional
from dataclasses import dataclass

from . import property_def as pdef
from . import types


@dataclass
class DataType:
    name: str
    description: Optional[str]
    extends: Optional['DataType']
    prop_defs: dict[str, 'pdef.PropertyDef']

    def type_for_path(self, path: list[str]) -> 'types.ValType':
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
                        f"Cannot evaluate path '{'.'.join(path)}' in data "
                        + f"type {self.name}: property '{head}' is of "
                        + f"scalar type '{pd.type}'."
                    )
            else:
                raise TypeError(
                    f"Cannot evaluate path '{'.'.join(path)}' in data type "
                    + f"{self.name}: no property or named '{head}'."
                )
