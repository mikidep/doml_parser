from typing import Optional
from dataclasses import dataclass

from . import types
from . import node_type as ntyp
from ..errors import TypeError


@dataclass
class Interface:
    name: str
    configure: 'ConfigureInterface'

    def _check(self, ctx: 'types.TypingCtx') -> None:
        self.configure._check(ctx)


@dataclass
class RunData:
    name: str
    type: 'types.ValType'
    value: 'types.Expr'

    def _check(self, ctx: 'types.TypingCtx') -> None:
        it, _ = types.infer_type(self.value, ctx)
        if it != self.type:
            raise TypeError(
                f"In interface run_data '{self.name}', expected type is "
                + f"{types.valtype_name(self.type)}, but the inferred type of "
                + f"the given expression is {types.valtype_name(it)}."
            )


@dataclass
class ConfigureInterface:
    ansible_path: str
    executor: Optional['ntyp.NodeType']
    run_data: dict[str, RunData]

    def _check(self, ctx: 'types.TypingCtx') -> None:
        for rd in self.run_data.values():
            rd._check(ctx)
