from dataclasses import dataclass
from typing import cast, TypeVar, Callable, Optional

import networkx as nx
import networkx.exception

from . import unres_rmdf_model as urm
from ...errors import StructureError


def _remove_all_edges(mdg: nx.MultiDiGraph, dg: nx.DiGraph) -> None:
    # In case of multiple edges between two nodes,
    # `MultiDiGraph.remove_edges_from` only removes one edge, so the
    # removal must be reiterated until a fixed point is reached.
    ol = len(mdg.edges)
    mdg.remove_edges_from(dg.edges)
    nl = len(mdg.edges)
    while nl < ol:
        ol = nl
        mdg.remove_edges_from(dg.edges)
        nl = len(mdg.edges)


_T = TypeVar("_T")
_CT = TypeVar("_CT")
_M = TypeVar("_M")


@dataclass
class UnresChecker:
    """Checks structural properties using unresolved models."""
    unres_rmdfs: list['urm.UnresRMDFModel']

    def run_preliminary_checks(self) -> None:
        self._check_data_types_acyclic()
        self._check_node_types_acyclic()
        self._check_data_type_composition_acyclic()
        self._check_node_types_templates_acyclic()

    def run_post_resolution_checks(self) -> None:
        self._check_data_type_overriding_cov()
        self._check_node_type_overriding_cov()

    def _check_circular_dependency(self,
                                   edges: list[tuple[str, str, str]],
                                   rel_name: str) -> None:
        mdg = nx.MultiDiGraph(edges)
        try:
            cycle = nx.find_cycle(mdg)
            raise StructureError(
                f"There is a circular dependency in {rel_name}:\n"
                + ";\n".join(f"{x} {rel} {y}"
                             for x, y, rel in cycle)
                + "."
            )
        except networkx.exception.NetworkXNoCycle:
            pass

    def _check_data_types_acyclic(self) -> None:
        edges = [
            (dt.name, dt.extends, "extends")
            for unres_rmdf in self.unres_rmdfs
            for dt in unres_rmdf.data_types.values()
            if dt.extends is not None
        ]
        self._check_circular_dependency(edges, "data type inheritance")

    def _check_node_types_acyclic(self) -> None:
        edges = [
            (nt.name, nt.extends, "extends")
            for unres_rmdf in self.unres_rmdfs
            for nt in unres_rmdf.node_types.values()
            if nt.extends is not None
        ]
        self._check_circular_dependency(edges, "node type inheritance")

    def _check_data_type_composition_acyclic(self) -> None:
        edges = [
            (dt.name, pdef.type, cast(str, "has a property of type"))
            for unres_rmdf in self.unres_rmdfs
            for dt in unres_rmdf.data_types.values()
            for pdef in dt.prop_defs.values()
        ] + [
            (dt.name, dt.extends, cast(str, "extends"))
            for unres_rmdf in self.unres_rmdfs
            for dt in unres_rmdf.data_types.values()
            if dt.extends is not None
        ]
        self._check_circular_dependency(edges, "data type composition")

    def _check_node_types_templates_acyclic(self) -> None:
        edges = [
            (nt.name, ntpl.type, cast(str, "declares a node template of type"))
            for unres_rmdf in self.unres_rmdfs
            for nt in unres_rmdf.node_types.values()
            for ntpl in nt.node_templates.values()
        ] + [
            (nt.name, nt.extends, cast(str, "extends"))
            for unres_rmdf in self.unres_rmdfs
            for nt in unres_rmdf.node_types.values()
            if nt.extends is not None
        ]
        self._check_circular_dependency(
            edges,
            "the relationship between a node type and the associated node "
            + "templates"
        )

    def _check_overriding_cov(
        self,
        get_types: Callable[['urm.UnresRMDFModel'], dict[str, _T]],
        name: Callable[[_T], str],
        extends: Callable[[_T], Optional[str]],
        get_cov_types: Callable[['urm.UnresRMDFModel'], dict[str, _CT]],
        cov_name: Callable[[_CT], str],
        cov_extends: Callable[[_CT], Optional[str]],
        additional_cov_types: list[str],
        get_members: Callable[[_T], dict[str, _M]],
        covariant: Callable[[_M], str],
        tname_pl_cap: str,
        ctname: str,
        mname: str,
        mname_pl: str
    ) -> None:
        ts = [t for unres_rmdf in self.unres_rmdfs
              for t in get_types(unres_rmdf).values()]
        # The inheritance relationship is the reflexive transitive closure
        # of the 'extends' relationship.
        t_inh = nx.DiGraph()
        t_inh.add_nodes_from([name(t) for t in ts])
        t_inh.add_edges_from([
            (name(t), extends(t))
            for t in ts
            if extends(t) is not None
        ])
        t_inh = nx.transitive_closure(t_inh, reflexive=True)
        t_inh = cast(nx.DiGraph, t_inh)

        cts = [ct for unres_rmdf in self.unres_rmdfs
               for ct in get_cov_types(unres_rmdf).values()]
        ct_inh = nx.DiGraph()
        ct_inh.add_nodes_from([cov_name(ct) for ct in cts])
        ct_inh.add_edges_from([
            (cov_name(ct), cov_extends(ct))
            for ct in cts
            if cov_extends(ct) is not None
        ])
        ct_inh.add_nodes_from(additional_cov_types)
        ct_inh = nx.transitive_closure(ct_inh, reflexive=True)
        ct_inh = cast(nx.DiGraph, ct_inh)
        # In this graph, two member types mt_1 and mt_2 are connected if they
        # are the types of the same member in types t_1 and t_2 such that t_1
        # extends t_2.
        member_ovr = nx.MultiDiGraph()
        ets = [(t, et) for t in ts for et in ts
               if t_inh.has_edge(name(t), name(et))]
        for t, et in ets:
            for m_name in get_members(t):
                if m_name in get_members(et):
                    u = covariant(get_members(t)[m_name])
                    v = covariant(get_members(et)[m_name])
                    k = (name(t), name(et), m_name)
                    member_ovr.add_edge(u, v, k)
        # The edges from t_inh are removed from member_ovr to leave only the
        # edges that violate the "covariance" between types and overridden
        # members.
        _remove_all_edges(member_ovr, ct_inh)

        if member_ovr.edges:
            raise StructureError(
                f"{tname_pl_cap} and types of overridden {mname_pl} are not "
                + "covariant:\n" + ";\n".join(
                    f"{t} overrides {mname} '{m}' inherited from {et}, "
                    + f"but {ctname} {u} is not a subtype of {v}"
                    for u, v, (t, et, m) in member_ovr.edges
                ) + "."
            )

    def _check_data_type_overriding_cov(self) -> None:
        # Data types and property data types
        self._check_overriding_cov(
            lambda unres_rmdf: unres_rmdf.data_types,
            lambda dt: dt.name,
            lambda dt: dt.extends,
            lambda unres_rmdf: unres_rmdf.data_types,
            lambda dt: dt.name,
            lambda dt: dt.extends,
            ["String", "Integer", "Float", "Boolean"],
            lambda dt: dt.prop_defs,
            lambda pd: pd.type,
            "Data types",
            "data type",
            "property",
            "properties"
        )

    def _check_node_type_overriding_cov(self) -> None:
        # Node types and property data types
        self._check_overriding_cov(
            lambda unres_rmdf: unres_rmdf.node_types,
            lambda nt: nt.name,
            lambda nt: nt.extends,
            lambda unres_rmdf: unres_rmdf.data_types,
            lambda dt: dt.name,
            lambda dt: dt.extends,
            ["String", "Integer", "Float", "Boolean"],
            lambda nt: nt.prop_defs,
            lambda pd: pd.type,
            "Node types",
            "data type",
            "property",
            "properties"
        )

        # Node types and edge node types
        self._check_overriding_cov(
            lambda unres_rmdf: unres_rmdf.node_types,
            lambda nt: nt.name,
            lambda nt: nt.extends,
            lambda unres_rmdf: unres_rmdf.node_types,
            lambda nt: nt.name,
            lambda nt: nt.extends,
            [],
            lambda nt: nt.edges,
            lambda edge: edge.type,
            "Node types",
            "node type",
            "edge",
            "edges"
        )

        # Node types and node template types
        self._check_overriding_cov(
            lambda unres_rmdf: unres_rmdf.node_types,
            lambda nt: nt.name,
            lambda nt: nt.extends,
            lambda unres_rmdf: unres_rmdf.node_types,
            lambda nt: nt.name,
            lambda nt: nt.extends,
            [],
            lambda nt: nt.node_templates,
            lambda ntpl: ntpl.type,
            "Node types",
            "node type",
            "node template",
            "node templates"
        )
