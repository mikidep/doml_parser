from . import unres_types as ut


class UnresOutput:
    def __init__(self,
                 name: str,
                 o_dict: dict) -> None:
        self.name = name
        self.type: ut.UnresValType = o_dict["type"]
        self.value: ut.UnresExpr = ut.raw_to_unres_expr(o_dict["value"])
