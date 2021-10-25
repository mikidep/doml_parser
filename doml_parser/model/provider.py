from dataclasses import dataclass

from .property_def import PropertyDef


@dataclass
class Provider:
    alias: str
    features: dict[str, PropertyDef]
