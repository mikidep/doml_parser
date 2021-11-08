from typing import cast
from dataclasses import dataclass

from . import node_type as ntyp
from .ntpl_property import NTplProperty
from .interface import Interface
from .capability import Capability
from .data import Data
from . import types
from ..errors import TypeError


@dataclass
class NodeTemplate:
    name: str
    type: 'ntyp.NodeType'
    properties: list[NTplProperty]
    relationships: list[tuple[str, 'NodeTemplate']]
    interfaces: dict[str, Interface]
    capabilities: dict[str, Capability]

    def _check(self, ctx: 'types.TypingCtx') -> None:
        for p in self.properties:
            try:
                self.type.type_for_path(p.path)
            except TypeError:
                raise TypeError(
                    f"In node template '{self.name}' of type {self.type.name}:"
                    + " invalid property path '" + ".".join(p.path) + "'."
                )
        own_prop_names = [p.path[0]
                          for p in self.properties
                          if len(p.path) == 1]
        missing_reqs = [p.name
                        for p in self.type.prop_defs.values()
                        if p.required and p.name not in own_prop_names]
        if missing_reqs:
            raise TypeError(
                f"In node template '{self.name}' of type {self.type.name}, the"
                + " following properties are required but not provided: "
                + ", ".join(missing_reqs) + "."
            )

        for p in self.properties:
            pname = ".".join(p.path)
            pval = p.value
            ptype, multiple = self.type.type_for_path(p.path)
            ptname = types.valtype_name(ptype)
            if multiple:
                if type(pval) is list:
                    pval = cast(list[types.Expr], pval)
                    for i, dv in enumerate(pval):
                        it, m = types.infer_type(dv, ctx)
                        if it != ptype:
                            raise TypeError(
                                f"In node template {self.name} of type "
                                + f"{self.type.name}: multiple-valued property"
                                + f" {pname} should have type {ptname}, but "
                                + "value given at index {i} has type "
                                + f"{types.valtype_name(it)}."
                            )
                        if m:
                            raise TypeError(
                                f"In node template {self.name} of type "
                                + f"{self.type.name}: cannot have nested "
                                + "multiple value in multiple-valued property "
                                + f"'{pname}' at index {i}."
                            )
                        if type(dv) is Data:
                            dv._check(ctx)
                else:
                    it, m = types.infer_type(cast(types.Expr, pval), ctx)
                    if it != ptype:
                        raise TypeError(
                            f"In node template {self.name} of type "
                            + f"{self.type.name}: property {pname} should have"
                            + f" type {ptname}, but value given has type "
                            + f"{types.valtype_name(it)}."
                        )
                    if not m:
                        raise TypeError(
                            f"In node template {self.name} of type "
                            + f"{self.type.name}: Property '{pname}' is "
                            + "multiple-valued, but value given is inferred to"
                            + " be a single value."
                        )
            else:
                if type(pval) is not list:
                    it, m = types.infer_type(cast(types.Expr, pval), ctx)
                    if it != ptype:
                        raise TypeError(
                            f"In node template {self.name} of type "
                            + f"{self.type.name}: property {pname} should have"
                            + f" type {ptname}, but value given has type "
                            + f"{types.valtype_name(it)}."
                        )
                    if m:
                        raise TypeError(
                            f"In node template {self.name} of type "
                            + f"{self.type.name}: Property '{pname}' is "
                            + "single-valued, but value given is inferred to "
                            + "be a multiple value."
                        )
                    if type(pval) is Data:
                        pval._check(ctx)
                else:
                    raise TypeError(
                        f"In node template {self.name} of type "
                        + f"{self.type.name}: Property '{pname}' is "
                        + "single-valued, but value given is a multiple value."
                    )

        for rname, rel in self.relationships:
            if (e := self.type.edges.get(rname)) is not None:
                if rel.type != e.type:
                    raise TypeError(
                        f"In node template {self.name} of type "
                        + f"{self.type.name}: edge {rname} has node type "
                        + f"{e.type.name}, but there is a relationship with "
                        + f"node template {rel.name} of type {rel.type.name}."
                    )

        for i in self.interfaces.values():
            i._check(ctx)
