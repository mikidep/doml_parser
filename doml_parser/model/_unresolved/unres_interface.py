from typing import Optional

from . import unres_types as ut

from . import resolver as r
from ..interface import Interface, ConfigureInterface, RunData
from ..types import map_opt


class UnresInterface:
    def __init__(self, name: str, i_dict: dict) -> None:
        self.name = name
        self.configure: UnresConfigureInterface \
            = UnresConfigureInterface(i_dict["configure"])

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> Interface:
        return Interface(self.name,
                         self.configure.resolve(resolver, ctx))


class UnresConfigureInterface:
    def __init__(self, ci_dict: dict) -> None:
        self.ansible_path: str = ci_dict["ansible_path"]
        self.executor: Optional[ut.Unres] = ci_dict.get("executor")
        self.run_data: dict[str, UnresRunData] \
            = {rdname: UnresRunData(rdname, rddict)
               for rdname, rddict in ci_dict.get("run_data", {}).items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> ConfigureInterface:
        executor = map_opt(lambda e: resolver.resolve_node_template(e, ctx),
                           self.executor)
        run_data = {rdname: rd.resolve(resolver, ctx)
                    for rdname, rd in self.run_data.items()}
        return ConfigureInterface(self.ansible_path,
                                  executor,
                                  run_data)


class UnresRunData:
    def __init__(self,
                 name: str,
                 rd_dict: dict) -> None:
        self.name = name
        self.type: ut.UnresValType = rd_dict["type"]
        self.value: ut.UnresExpr = ut.raw_to_unres_expr(rd_dict["value"])

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> RunData:
        vtype = ut.resolve_val_type(self.type, resolver, ctx)
        return RunData(
            self.name,
            vtype,
            ut.resolve_expr(self.value, vtype, resolver, ctx)
        )
