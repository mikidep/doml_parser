from typing import Callable, Optional, TypeVar
from dataclasses import dataclass

from ..types import map_or_else

from . import unres_model as um
from . import unres_rmdf_model as urm
from . import unres_node_type as untyp
from . import unres_node_template as untpl
from . import unres_data_type as udt
from . import unres_provider as up
from . import unres_types as ut

from ..node_type import NodeType
from ..node_template import NodeTemplate
from ..data_type import DataType
from ..provider import Provider

from ...errors import ReferenceNotFound, MultipleDefinitions, TypeError

from .unres_checker import UnresChecker


def _is_imported(ref: 'ut.Unres', ctx: 'ResolverCtx') -> bool:
    for impt in ctx.unres_model.imports:
        if impt[-1] == "*":
            if ref.startswith(impt[:-1]):
                return True
        elif ref == impt:
            return True
    return False


_T = TypeVar("_T")


class Resolver:
    def __init__(self,
                 unres_rmdfs: list['urm.UnresRMDFModel']) -> None:
        self.unres_rmdfs = unres_rmdfs

        self.node_types: dict[str, NodeType] = {}
        self.data_types: dict[str, DataType] = {}
        self.providers: dict[str, Provider] = {}

        checker = UnresChecker(self.unres_rmdfs)
        checker.run_preliminary_checks()
        self._resolve_types()
        checker.run_post_resolution_checks()

    def _resolve_types(self) -> None:
        for unres_rmdf in self.unres_rmdfs:
            ctx = ResolverCtx(unres_rmdf)
            for ntref in unres_rmdf.node_types:
                self.resolve_node_type(ntref, ctx)
            for dtref in unres_rmdf.data_types:
                self.resolve_data_type(dtref, ctx)

    def _find_in_rmdfs(
        self,
        ref: 'ut.Unres',
        accessor: Callable[['urm.UnresRMDFModel'], dict[str, _T]],
        type_name: str
    ) -> Optional[tuple[_T, 'urm.UnresRMDFModel']]:
        needles = [(accessor(ur)[ref], ur)
                   for ur in self.unres_rmdfs
                   if ref in accessor(ur)]
        if len(needles) == 0:
            return None
        elif len(needles) > 1:
            raise MultipleDefinitions(
                    f"Multiple definitions for {type_name} {ref}."
                )
        else:
            return needles[0]

    def _find_node_type(self, ntref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> Optional[tuple['untyp.UnresNodeType',
                              'um.UnresModel']]:
        if _is_imported(ntref, ctx):
            imp_nt = self._find_in_rmdfs(
                ntref,
                lambda unres_rmdf: unres_rmdf.node_types,
                "node type"
            )
        else:
            imp_nt = None
        if type(ctx.unres_model) is urm.UnresRMDFModel:
            nt = ctx.unres_model.node_types.get(ntref)
            if nt is not None:
                return (nt, ctx.unres_model)
            else:
                return imp_nt
        else:
            return imp_nt

    def resolve_node_type(self, ntref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> NodeType:
        # In order to return cached type, it must be visible
        if (_is_imported(ntref, ctx)
            or (type(ctx.unres_model) is urm.UnresRMDFModel
                and ntref in ctx.unres_model.node_types)) \
           and (nt := self.node_types.get(ntref)) is not None:
            return nt
        elif (unres_nt_r := self._find_node_type(ntref, ctx)) is not None:
            unresnt, unresrmdf = unres_nt_r
            nt = NodeType(unresnt.name,
                          unresnt.description,
                          unresnt.alias,
                          None,
                          {}, {}, {})
            self.node_types[ntref] = nt
            nt_ = unresnt.resolve(self, ResolverCtx(unresrmdf))
            nt.extends = nt_.extends
            nt.prop_defs = nt_.prop_defs
            nt.node_templates = nt_.node_templates
            nt.edges = nt_.edges
            return nt
        else:
            raise ReferenceNotFound(f"Could not find node type {ntref}.")

    def resolve_node_template(self, ntref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> NodeTemplate:
        if ctx.ntpl_ctx is not None:
            if (nt := ctx.ntpl_ctx.node_templates.get(ntref)) is not None:
                return nt
            elif (unresnt := ctx.ntpl_ctx.unres_node_templates.get(ntref)) \
                    is not None:
                nt = NodeTemplate(unresnt.name,
                                  self.resolve_node_type(
                                      unresnt.type,
                                      ctx
                                  ),
                                  [],
                                  [],
                                  {},
                                  {})
                ctx.ntpl_ctx.node_templates[ntref] = nt
                nt_ = unresnt.resolve(self, ctx)
                nt.properties = nt_.properties
                nt.relationships = nt_.relationships
                nt.interfaces = nt_.interfaces
                nt.capabilities = nt_.capabilities
                return nt
            else:
                raise ReferenceNotFound(
                    f"Could not find node template {ntref}."
                )
        else:
            raise TypeError("Cannot resolve node template without "
                            + "a node template context.")

    def _find_data_type(self, dtref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> Optional[tuple['udt.UnresDataType', 'urm.UnresRMDFModel']]:
        if _is_imported(dtref, ctx):
            imp_dt = self._find_in_rmdfs(
                dtref,
                lambda unres_rmdf: unres_rmdf.data_types,
                "data type"
            )
        else:
            imp_dt = None
        if type(ctx.unres_model) is urm.UnresRMDFModel:
            dt = ctx.unres_model.data_types.get(dtref)
            if dt is not None:
                return (dt, ctx.unres_model)
            else:
                return imp_dt
        else:
            return imp_dt

    def resolve_data_type(self, dtref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> DataType:
        # In order to return cached type, it must be visible
        if (_is_imported(dtref, ctx)
            or (type(ctx.unres_model) is urm.UnresRMDFModel
                and dtref in ctx.unres_model.data_types)) \
           and (dt := self.data_types.get(dtref)) is not None:
            return dt
        elif (unres_dt_r := self._find_data_type(dtref, ctx)) is not None:
            unresdt, unresrmdf = unres_dt_r
            dt = DataType(unresdt.name,
                          unresdt.description,
                          None,
                          {})
            self.data_types[dtref] = dt
            dt_ = unresdt.resolve(self, ResolverCtx(unresrmdf))
            dt.extends = dt_.extends
            dt.prop_defs = dt_.prop_defs
            return dt
        else:
            raise ReferenceNotFound(f"Could not find data type {dtref}.")

    def _find_provider(self, pref: 'ut.Unres') \
            -> Optional[tuple['up.UnresProvider', 'urm.UnresRMDFModel']]:
        return self._find_in_rmdfs(pref,
                                   lambda unres_rmdf: map_or_else(
                                       lambda p: {p.alias: p},
                                       {},
                                       unres_rmdf.provider
                                   ),
                                   "provider")

    def resolve_provider(self, pref: 'ut.Unres', ctx: 'ResolverCtx') \
            -> Provider:
        if (p := self.providers.get(pref)) is not None:
            return p
        elif (unres_p_r := self._find_provider(pref)) is not None:
            unresp, unresrmdf = unres_p_r
            p = unresp.resolve(self, ResolverCtx(unresrmdf))
            self.providers[pref] = p
            return p
        else:
            raise ReferenceNotFound(f"Could not find provider {pref}.")


@dataclass
class NodeTplCtx:
    unres_node_templates: dict[str, 'untpl.UnresNodeTemplate']
    node_templates: dict[str, NodeTemplate]


@dataclass
class ResolverCtx:
    unres_model: 'um.UnresModel'
    ntpl_ctx: Optional[NodeTplCtx] = None
