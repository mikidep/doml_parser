from typing import Optional

from . import unres_types as ut


class UnresInterface:
    def __init__(self, name: str, i_dict: dict) -> None:
        self.name = name
        self.configure: UnresConfigureInterface \
            = UnresConfigureInterface(i_dict["configure"])


class UnresConfigureInterface:
    def __init__(self, ci_dict: dict) -> None:
        self.ansible_path: str = ci_dict["ansible_path"]
        self.executor: Optional[ut.Unres] = ci_dict.get("executor")
        self.run_data: dict[str, ut.UnresExpr] \
            = {k: ut.raw_to_unres_expr(v)
               for k, v in ci_dict.get("run_data", {}).items()}
