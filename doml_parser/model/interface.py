from typing import Optional
from dataclasses import dataclass

from . import types
from . import node_template as ntpl


@dataclass
class Interface:
    name: str
    configure: 'ConfigureInterface'


@dataclass
class RunData:
    name: str
    type: 'types.ValType'
    value: 'types.Expr'


@dataclass
class ConfigureInterface:
    ansible_path: str
    executor: Optional['ntpl.NodeTemplate']
    run_data: dict[str, RunData]
