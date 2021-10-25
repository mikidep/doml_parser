from . import unres_types as ut


class UnresEdge:
    def __init__(self, name: str, e_dict: dict) -> None:
        self.name = name
        self.type: ut.Unres = e_dict["type"]
        self.attribute: str = e_dict["attribute"]
