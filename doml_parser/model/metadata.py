from typing import Optional
from dataclasses import dataclass

from .provider import Provider


@dataclass
class Metadata:
    version: str
    provider: Optional[Provider]
    description: Optional[str]
