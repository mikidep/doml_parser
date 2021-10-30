from typing import Union, cast
from dataclasses import dataclass

from . import types
from . import data_type as dtyp
from ..errors import TypeError


@dataclass
class Data:
    type: 'dtyp.DataType'
    properties: dict[str, Union['types.Expr', list['types.Expr']]]

    def _check(self, ctx: 'types.TypingCtx') -> None:
        undef_props = [p for p in self.properties
                       if p not in self.type.prop_defs]
        if undef_props:
            raise TypeError(
                f"In instance of data type {self.type.name}, the following "
                + "properties are not defined: "
                + ", ".join(undef_props) + "."
            )

        missing_reqs = [p.name
                        for p in self.type.prop_defs.values()
                        if p.required and p.name not in self.properties]
        if missing_reqs:
            raise TypeError(
                f"In instance of data type {self.type.name}, the following "
                + "properties are required but not provided: "
                + ", ".join(missing_reqs) + "."
            )

        for pname, pval in self.properties.items():
            ptype = self.type.prop_defs[pname].type
            ptname = types.valtype_name(ptype)
            if self.type.prop_defs[pname].multiple:
                if type(pval) is list:
                    pval = cast(list[types.Expr], pval)
                    for i, dv in enumerate(pval):
                        it, m = types.infer_type(dv, ctx)
                        if it != ptype:
                            raise TypeError(
                                f"In instance of data type {self.type.name}: "
                                + f"multiple-valued property {pname} should "
                                + f"have type {ptname}, but value given at "
                                + f"index {i} has type "
                                + f"{types.valtype_name(it)}."
                            )
                        if m:
                            raise TypeError(
                                f"In instance of data type {self.type.name}: "
                                + "cannot have a nested multiple value for "
                                + "multiple-valued property {pname} at index"
                                + f"{i}."
                            )
                        if type(dv) is Data:
                            dv._check(ctx)
                else:
                    it, m = types.infer_type(cast(types.Expr, pval), ctx)
                    if it != ptype:
                        raise TypeError(
                            f"In instance of data type {self.type.name}: "
                            + f"property {pname} should have type {ptname}, "
                            + "but value given has type "
                            + f"{types.valtype_name(it)}."
                        )
                    if not m:
                        raise TypeError(
                            f"In instance of data type {self.type.name}: "
                            + f"Property '{pname}' is multiple-valued, but "
                            + "value given is inferred to be a single value."
                        )
            else:
                if type(pval) is not list:
                    it, m = types.infer_type(cast(types.Expr, pval), ctx)
                    if it != ptype:
                        raise TypeError(
                            f"In instance of data type {self.type.name}: "
                            + f"property {pname} should have type {ptname}, "
                            + "but value given has type "
                            + f"{types.valtype_name(it)}."
                        )
                    if m:
                        raise TypeError(
                            f"In instance of data type {self.type.name}: "
                            + f"Property '{pname}' is single-valued, but value"
                            + " given is inferred to be a multiple value."
                        )
                    if type(pval) is Data:
                        pval._check(ctx)
                else:
                    raise TypeError(
                        f"In instance of data type {self.type.name}: Property "
                        + f"'{pname}' is single-valued, but value given is a"
                        + " multiple value."
                    )
