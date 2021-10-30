from dataclasses import dataclass

from .property_def import PropertyDef
from .types import TypingCtx


@dataclass
class Provider:
    alias: str
    features: dict[str, PropertyDef]

    def _check(self) -> None:
        for f in self.features.values():
            f._check(TypingCtx(None, None))
