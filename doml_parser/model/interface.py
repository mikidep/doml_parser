from typing import Optional
from dataclasses import dataclass

from .types import Expr
from . import node_template as ntpl


@dataclass
class Interface:
    name: str
    configure: 'ConfigureInterface'


@dataclass
class ConfigureInterface:
    ansible_path: str
    executor: Optional['ntpl.NodeTemplate']
    run_data: dict[str, Expr]
