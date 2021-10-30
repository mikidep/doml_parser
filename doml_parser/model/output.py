from dataclasses import dataclass

from .types import Expr, ValType, infer_type, TypingCtx, valtype_name


@dataclass
class Output:
    name: str
    type: ValType
    value: Expr

    def _check(self, ctx: TypingCtx) -> None:
        it, _ = infer_type(self.value, ctx)
        if it != self.type:
            raise TypeError(
                f"In output '{self.name}', expected type is "
                + f"{valtype_name(self.type)}, but the inferred type of "
                + f"the given expression is {valtype_name(it)}."
            )
