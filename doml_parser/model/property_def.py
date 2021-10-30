from typing import Optional, Union, cast
from dataclasses import dataclass

from . import types
from .data import Data
from ..errors import TypeError


@dataclass
class PropertyDef:
    name: str
    type: 'types.ValType'
    description: Optional[str]
    required: bool
    multiple: bool
    default: Optional[Union['types.Expr', list['types.Expr']]]
    context: str
    is_input: bool

    def _check(self, ctx: 'types.TypingCtx') \
            -> None:
        pd_string = "Input" if self.is_input else "Property definition"
        if self.default is not None:
            if self.multiple:
                if type(self.default) is list:
                    for i, dv in enumerate(self.default):
                        it, m = types.infer_type(dv, ctx)
                        if it != self.type:
                            raise TypeError(
                                f"{pd_string} '{self.name}' of "
                                + f"{self.context} has type "
                                + f"{types.valtype_name(self.type)}, but "
                                + "default value of type "
                                + f"{types.valtype_name(it)} at index {i}."
                            )
                        if m:
                            raise TypeError(
                                f"{pd_string} '{self.name}' of {self.context}:"
                                + " cannot have nested multiple values in"
                                + f"given default value at index {i}."
                            )
                        if type(dv) is Data:
                            dv._check(ctx)
                else:
                    it, m = types.infer_type(cast(types.Expr, self.default),
                                             ctx)
                    if it != self.type:
                        raise TypeError(
                            f"{pd_string} '{self.name}' of "
                            + f"{self.context} has type "
                            + f"{types.valtype_name(self.type)}, but default "
                            + f"value of type {types.valtype_name(it)}."
                        )
                    if not m:
                        raise TypeError(
                            f"{pd_string} '{self.name}' of {self.context} "
                            + "is multiple-valued, but its default value is "
                            + "inferred to be a single value."
                        )
            else:
                if type(self.default) is not list:
                    it, m = types.infer_type(cast(types.Expr, self.default),
                                             ctx)
                    if it != self.type:
                        raise TypeError(
                            f"{pd_string} '{self.name}' of "
                            + f"{self.context} has type "
                            + f"{types.valtype_name(self.type)}, but default "
                            + f"value of type {types.valtype_name(it)}."
                        )
                    if m:
                        raise TypeError(
                            f"{pd_string} '{self.name}' of {self.context} "
                            + "is single-valued, but its default value is "
                            + "inferred to be a multiple value."
                        )
                    if type(self.default) is Data:
                        self.default._check(ctx)
                else:
                    raise TypeError(
                        f"{pd_string} '{self.name}' of {self.context} "
                        + "is single-valued, but its default value is a "
                        + "multiple value."
                    )
