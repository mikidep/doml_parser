from typing import Optional
from dataclasses import dataclass

from . import types
from . import node_type as ntyp


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
    executor: Optional['ntyp.NodeType']
    run_data: dict[str, RunData]
